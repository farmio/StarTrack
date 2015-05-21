from time import sleep

import RPi.GPIO as GPIO

import position
import distance
from delegate import delegate
from display import display


position.rotation_callback = delegate(position.rotation_callback)

@position.rotation_callback.callback_async
def update_display():
    display.update(position.rotation_count)

try:
    print 'Waiting for Interrupt'
    while 1:
        pass

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
