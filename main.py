from time import sleep
from threading import Lock

import RPi.GPIO as GPIO

from position import Sensor
from distance import hose
from delegate import Delegate
from delegate import Queue
from display import display


display.init()

#set delegates
Sensor.rotation_callback = Delegate(Sensor.rotation_callback)
Sensor.sensor_callback = Delegate(Sensor.sensor_callback)

#initialise threads
display_thread = Lock()

def sensor_update():
    display.sensor_update(Sensor.sensor_buffer, Sensor.direction_buffer)

def rotation_update():
    display.rotation_update(Sensor.rotation_count)

@Sensor.rotation_callback.callback
def display_rotation(*args, **kwargs):
    Queue(rotation_update,
          display_thread,
          rest=0.01).start()

@Sensor.sensor_callback.callback
def display_sensor(*args, **kwargs):
    Queue(sensor_update,
          display_thread,
          rest=0.01).start()

try:
    print 'Waiting for Interrupt'
    while 1:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
