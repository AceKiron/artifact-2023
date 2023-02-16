# Includes MicroPython SSD1306 OLED driver, I2C and SPI interfaces

from machine import Pin, I2C
from micropython import const
import framebuf

class Application:
    def __init__(self):
        self.SleepTime = 0

        self.enabled = True

        self.Init()
    
    def Init(self):
        pass
    
    def Update(self):
        pass
    
    def Stop(self):
        self.enabled = False
    
    def Run(self):
        while self.enabled:
            self.Update()

            if self.SleepTime > 0:
                time.sleep(self.SleepTime)

class Input:
    def __init__(self, pin):
        if pin != None:
            self.pin = Pin(pin, Pin.IN)

    def Read(self):
        return self.pin.value()
    
    def Print(self):
        print(self.pin.value())

class Keypad4x4(Input):
    Keys = ["1", "2", "3", "A",
            "4", "5", "6", "B",
            "7", "8", "9", "C",
            "*", "0", "#", "D"]
    
    def __init__(self, keypad_rows, keypad_columns):
        super().__init__(None)

        self.row_pins = []
        self.col_pins = []
        
        for x in range(4):
            self.row_pins.append(Pin(keypad_rows[x], Pin.OUT))
            self.row_pins[x].value(1)
            
            self.col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
            self.col_pins[x].value(0)
    
    def Read(self):
        for row in range(4):
            self.row_pins[row].high()
            
            for col in range(4):
                if self.col_pins[col].value() == 1:
                    self.row_pins[row].low()
                    return row * 4 + col
                
            self.row_pins[row].low()

class SSD1306(framebuf.FrameBuffer):
    # register definitions
    SET_CONTRAST = const(0x81)
    SET_ENTIRE_ON = const(0xA4)
    SET_NORM_INV = const(0xA6)
    SET_DISP = const(0xAE)
    SET_MEM_ADDR = const(0x20)
    SET_COL_ADDR = const(0x21)
    SET_PAGE_ADDR = const(0x22)
    SET_DISP_START_LINE = const(0x40)
    SET_SEG_REMAP = const(0xA0)
    SET_MUX_RATIO = const(0xA8)
    SET_COM_OUT_DIR = const(0xC0)
    SET_DISP_OFFSET = const(0xD3)
    SET_COM_PIN_CFG = const(0xDA)
    SET_DISP_CLK_DIV = const(0xD5)
    SET_PRECHARGE = const(0xD9)
    SET_VCOM_DESEL = const(0xDB)
    SET_CHARGE_PUMP = const(0x8D)

    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            self.SET_DISP | 0x00,  # off
            # address setting
            self.SET_MEM_ADDR,
            0x00,  # horizontal
            # resolution and layout
            self.SET_DISP_START_LINE | 0x00,
            self.SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
            self.SET_MUX_RATIO,
            self.height - 1,
            self.SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
            self.SET_DISP_OFFSET,
            0x00,
            self.SET_COM_PIN_CFG,
            0x02 if self.width > 2 * self.height else 0x12,
            # timing and driving scheme
            self.SET_DISP_CLK_DIV,
            0x80,
            self.SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            self.SET_VCOM_DESEL,
            0x30,  # 0.83*Vcc
            # display
            self.SET_CONTRAST,
            0xFF,  # maximum
            self.SET_ENTIRE_ON,  # output follows RAM contents
            self.SET_NORM_INV,  # not inverted
            # charge pump
            self.SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            self.SET_DISP | 0x01,
        ):  # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(self.SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(self.SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(self.SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(self.SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(self.SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(self.SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)

class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, scl, sda, freq=200000, addr=0x3C, external_vcc=False):
        self.i2c = I2C(0, scl=Pin(scl), sda=Pin(sda), freq=freq)
        self.addr = addr
        self.temp = bytearray(2)
        self.write_list = [b"\x40", None]  # Co=0, D/C#=1
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.write_list[1] = buf
        self.i2c.writevto(self.addr, self.write_list)
