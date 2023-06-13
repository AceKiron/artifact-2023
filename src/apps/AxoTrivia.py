from utils import Typewriter, random_shuffle, putTextOnOLED, ButtonPressListener
import picosquared as ps
import utime
import random

#https://axolotlapi.kirondevcoder.repl.co/trivia/multipleQuestions.json
trivia_questions = [
    {
        "question": "Which lake are we native to?",
        "correct_answer": "Lake Xochimilco (Valley of Mexico, Mexico)",
        "incorrect_answers": [
            "Lake Patzcuaro (Michoacan, Mexico)",
            "Crater Lake (Oregon, USA)",
            "Laguna Bacalar (Belize Border, Mexico)"
        ]
    },
    {
        "question": "Our species is named after which Aztec god?",
        "correct_answer": "Xolotl",
        "incorrect_answers": [
            "Ixtlilton",
            "Patecatl",
            "Xiuhtecuhtli"
        ]
    },
    {
        "question": "What pH value is ideal for us?",
        "correct_answer": "7.4 - 7.6",
        "incorrect_answers": [
            "7.0 - 7.2",
            "7.2 - 7.4",
            "7.6 - 7.8"
        ]
    },
    {
        "question": "What nitrate level is acceptable for us?",
        "correct_answer": "20 - 60 ppm",
        "incorrect_answers": [
            "0 - 20 ppm",
            "60 - 100 ppm",
            "100+ ppm"
        ]
    },
    {
        "question": "What's our average lifespan?",
        "correct_answer": "10 - 15 years",
        "incorrect_answers": [
            "0 - 5 years",
            "5 - 10 years",
            "15 - 20 years"
        ]
    },
    {
        "question": "What class in endangerment do we fall in?",
        "correct_answer": "Critically endangered",
        "incorrect_answers": [
            "Vulnerable",
            "Extinct in the wild",
            "Least Concern"
        ]
    }
]

class Game:
    def __init__(self):
        self.chooseQuestion()
        
    def chooseQuestion(self):
        q = random.choice(trivia_questions)
        
        self.question = q["question"]
        self.answers = random_shuffle([q["correct_answer"], q["incorrect_answers"][0], q["incorrect_answers"][1], q["incorrect_answers"][2]])
        self.correct_index = self.answers.index(q["correct_answer"])
        
        self.hasAnswered = False
    
    def guess(self, index, onCorrect, onIncorrect):
        self.hasAnswered = True
        
        if self.correct_index == index:
            onCorrect()
        else:
            onIncorrect()

class MyState(ps.State):
    def __init__(self, keypad, oled):
        self.keypad = keypad
        self.oled = oled
        
        self.game = Game()
        
        self.typewriter = Typewriter()
        self.buttonPressListener = ButtonPressListener(
            initialValue = self.keypad.read()
        )
        
        self.setPage(0)
        
    def setPage(self, page):
        self.page = page
        
        if page == 0:
            self.typewriter.setTargetText(self.game.question)
        elif page == 1:
            self.typewriter.setTargetText("A:" + self.game.answers[0])
        elif page == 2:
            self.typewriter.setTargetText("B:" + self.game.answers[1])
        elif page == 3:
            self.typewriter.setTargetText("C:" + self.game.answers[2])
        elif page == 4:
            self.typewriter.setTargetText("D:" + self.game.answers[3])
        elif page == 5:
            self.typewriter.setTargetText("Correct! :D")
        elif page == 6:
            self.typewriter.setTargetText("Incorrect. :C")
    
    def onCorrect(self):
        self.setPage(5)
    
    def onIncorrect(self):
        self.setPage(6)
    
    def update(self):
        self.typewriter.increment()
        
        putTextOnOLED(self.oled, self.typewriter.getText())
        
        value = self.keypad.read()
        
        if self.buttonPressListener.update(value):
            if self.game.hasAnswered:
                if not self.typewriter.isTyping():
                    utime.sleep(1)
                    self.game.chooseQuestion()
                    self.setPage(0)
            else:
                # Navigeer tussen tekstblokken
                if value == 12: # *
                    newPage = self.page - 1
                    if newPage == -1:
                        newPage = 0
                    self.setPage(newPage)
                    
                    utime.sleep(0.1)
                elif value == 14: # #
                    newPage = self.page + 1
                    if newPage == 5:
                        newPage = 4
                    self.setPage(newPage)
                    
                    utime.sleep(0.1)
                        
                # Kies antwoorden
                elif value == 3: # A
                    self.game.guess(0, self.onCorrect, self.onIncorrect)
                elif value == 7: # B
                    self.game.guess(1, self.onCorrect, self.onIncorrect)
                elif value == 11: # C
                    self.game.guess(2, self.onCorrect, self.onIncorrect)
                elif value == 15: # D
                    self.game.guess(3, self.onCorrect, self.onIncorrect)
        
        self.lastButtonPress = value
