from time import sleep
from threading import Lock

import RPi.GPIO as GPIO

from position import Sensor
from distance import hose
from delegate import Delegate
from delegate import Queue
from display import Display


display = Display(Sensor)

#set delegates
Sensor.rotation_callback = Delegate(Sensor.rotation_callback)
Sensor.sensor_callback = Delegate(Sensor.sensor_callback)

#initialise threads
display_thread = Lock()

@Sensor.rotation_callback.callback
def display_rotation(*args, **kwargs):
    Queue(display.rotation_update,
          display_thread,
          rest=0.01).start()

@Sensor.sensor_callback.callback
def display_sensor(*args, **kwargs):
    Queue(display.sensor_update,
          display_thread,
          rest=0.01).start()

try:
    print 'Waiting for Interrupt'
    while 1:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
