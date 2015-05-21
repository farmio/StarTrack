from time import sleep

import RPi.GPIO as GPIO

import position
from display import display
import distance


try:
    print 'Waiting for Interrupt'
    while 1:
        display.clear()
        display.set_cursor(0, 0)
        display.message(str(position.rotation_count))
        sleep(2)
        print 'rotation_count: %r'%position.rotation_count

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
