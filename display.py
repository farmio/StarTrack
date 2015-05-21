import time
import math

import Adafruit_CharLCD as AdaLCD

from config import lcd

display = AdaLCD.Adafruit_CharLCD(lcd['rs'],
                                  lcd['en'],
                                  lcd['d4'],
                                  lcd['d5'],
                                  lcd['d6'],
                                  lcd['d7'],
                                  lcd['columns'],
                                  lcd['rows']
                                  )

#display.message('Hello world! ')
#display.set_cursor(0, 1)
#display.message('at 0, 1 now')
