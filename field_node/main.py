from time import sleep
from threading import Lock
from config import Config

import RPi.GPIO as GPIO

from modules import *

# load config
f = file('config.cfg')
cfg = Config(f)


# Set up modules

# Proximity Sensors need 2nd argument 1 or 2
sensor_one = Proximity_Sensor(cfg.gpio_pins.sensors['front'],
                              cfg.rot_sensors,
                              1)
sensor_two = Proximity_Sensor(cfg.gpio_pins.sensors['rear'],
                              cfg.rot_sensors,
                              2)

distance = Distance(cfg.reel)
pace = Pace()
status = Status(distance, pace)

display = Display(cfg.gpio_pins.display, cfg.lcd, status)
buttons = init_buttons(cfg.gpio_pins.buttons, cfg.buttons)
menu = init_menu(display, buttons, status)

Http_Client(cfg.private.http, status, cfg.general['id'])
UMTS(cfg.network.sakis3g)
UMTS.set_callbacks(status)
# adn = Adn(private.adn)

# set delegates
Rotation.signal = Delegate(Rotation.signal)
Rotation.sensor_signal = Delegate(Rotation.sensor_signal)
status.sensor_update = Delegate(status.sensor_update)
status.rotation_update = Delegate(status.rotation_update)
status.start_report = Delegate(status.start_report)
status.stop_report = Delegate(status.stop_report)
status.umts_connected = Delegate(status.umts_connected)
# status.layer_update = Delegate(status.layer_update)
# status.row_update = Delegate(status.row_update)
# Alert.now = Delegate(Alert.now)

# initialise thread locks
# display_thread = Lock()
# network_thread = Lock()

# attach Sensors to status
Rotation.signal += status.rotation_update
Rotation.sensor_signal += status.sensor_update

status.reconnect_umts = UMTS.connect
status.disconnect_umts = UMTS.disconnect


@status.rotation_update.callback
def on_rotation_update(*args, **kwargs):
    display.rotation_update()
    if status.reporting:
        Http_Client.update_skip()


@status.sensor_update.callback
def on_sensor_update(*args, **kwargs):
    display.sensor_update()


@status.start_report.callback
def on_start_report(*args, **kwargs):
    Http_Client.sign_in()


@status.stop_report.callback
def on_stop_report(*args, **kwargs):
    Http_Client.sign_out()
    # UMTS.disconnect()


# @Alert.now.callback
# def network_callback(*args, **kwargs):
#     Queue(adn.pm, network_thread).start()

try:
    i = 0
    print('Waiting for Interrupt')
    while i < 5:
        i += 1
        status.rotation_update(1)
    while 1:
        sleep(1)
        i += 1
        if i > 1000000:
            print('i = ', i)
            i = 0
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
