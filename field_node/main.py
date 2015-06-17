from time import sleep
from threading import Lock

import RPi.GPIO as GPIO

import config
import private              #for access-tokens / mail-configuration
from modules import *


#Sensors need 2nd argument 1 or 2
sensor_one = Sensor(config.rot_sensors['front'], 1)
sensor_two = Sensor(config.rot_sensors['rear'], 2)

distance = Distance(config.reel)
pace = Pace()
status = Status(distance, pace)
display = Display(config.lcd, status)
#adn = Adn(private.adn)

#set delegates
Rotation.signal = Delegate(Rotation.signal)
Rotation.sensor_signal = Delegate(Rotation.sensor_signal)
status.sensor_update = Delegate(status.sensor_update)
status.rotation_update = Delegate(status.rotation_update)
status.layer_update = Delegate(status.layer_update)
status.row_update = Delegate(status.row_update)
#Alert.now = Delegate(Alert.now)

#initialise thread locks
display_thread = Lock()
#network_thread = Lock()

@Rotation.signal.callback
def on_rotation_signal(*args, **kwargs):
    #this triggers rotation_count calculation
    status.rotation_update(*args, **kwargs)
    #Alert.spy(*args, **kwargs)
    #Queue(display.rotation_update,
    #      display_thread,
    #      pause=0.01).start()

@Rotation.sensor_signal.callback
def on_sensor_signal(*args, **kwargs):
    #this happens before rotation_count calculation
    status.sensor_update(*args, **kwargs)
    #Queue(display.sensor_update,
    #      display_thread,
    #      pause=0.01).start()

display_rotation = lambda x: Queue(display.rotation_update,
                                   display_thread,
                                   pause=0.01).start()

display_sensors = lambda x: Queue(display.sensor_update,
                                  display_thread,
                                  pause=0.01).start()

def attatch_display():
    status.rotation_update += display_rotation
    status.sensor_update += display_sensors
    #status.layer_update += display.layer

def detatch_display():
    status.rotation_update -= display_rotation
    status.sensor_update -= display_sensors

attatch_display()

def start_monitoring():
    try:                #not very beautiful
        spy
    except NameError:                   #target
        spy = Spy(status.speed_last_mh, 500, config.monitoring)

def stop_monitoring():
    del spy     #????????????????????? doesnot touch thread

start_monitoring()

#@Alert.now.callback
#def network_callback(*args, **kwargs):
#    Queue(adn.pm, network_thread).start()

try:
    print('Waiting for Interrupt')
    while 1:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
