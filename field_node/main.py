from time import sleep
from threading import Lock

import RPi.GPIO as GPIO

import config
import private              #for access-tokens / mail-configuration
from modules import Sensor
from modules import Hose
from modules import Delegate
from modules import Queue
from modules import Display
from modules import Pace
from modules import Status
from modules import Adn
from modules import Alert


#Sensors need 2nd argument 1 or 2
sensor_one = Sensor(config.rot_sensors['front'], 1)
sensor_two = Sensor(config.rot_sensors['rear'], 2)

hose = Hose(config.reel)
pace = Pace()
status = Status(Sensor, hose, pace)
display = Display(config.lcd, status)
adn = Adn(private.adn)

#set delegates
Sensor.rotation_callback = Delegate(Sensor.rotation_callback)
Sensor.sensor_callback = Delegate(Sensor.sensor_callback)
Alert.now = Delegate(Alert.now)

@Sensor.rotation_callback.callback
def rotation(*args, **kwargs):
    pace.callback(*args, **kwargs)
    Alert.spy(*args, **kwargs)

#initialise thread locks for display
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

#initialise thread locks for networking
network_thread = Lock()

@Alert.now.callback
def network_callback(*args, **kwargs):
    Queue(adn.pm, network_thread).start()


try:
    print('Waiting for Interrupt')
    while 1:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
