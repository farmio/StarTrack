import time
import math

import Adafruit_CharLCD as AdaLCD

from config import lcd

def update(self, data):
    self.clear()
    self.set_cursor(0, 0)
    self.message(str(data))


AdaLCD.Adafruit_CharLCD.update = update

display = AdaLCD.Adafruit_CharLCD(lcd['rs'],
                                  lcd['en'],
                                  lcd['d4'],
                                  lcd['d5'],
                                  lcd['d6'],
                                  lcd['d7'],
                                  lcd['columns'],
                                  lcd['rows']
                                  )
