import RPi.GPIO as GPIO

from config import rot_sensors

__all__ = ['rotation_count']  #only this can be exported using *

GPIO.setmode(GPIO.BCM)

rotation_count = 0
sensor_buffer = {
    1: False,
    2: False
}
direction_buffer = 0

def rotation_callback(direction):
    global rotation_count

    rotation_count += direction
    print 'rotation_count: %r'%rotation_count

def sensor_callback(status, sensor_location):
    print('callback on sensor %r'%sensor_location)
    print('callback: %r'%status)

    global direction_buffer

    sensor_buffer[sensor_location] = status

    if sensor_buffer[1] == sensor_buffer[2]:
        if sensor_location == 1:
            direction_buffer -= 1   #right
        elif sensor_location == 2:
            direction_buffer += 1   #left
    else:
        if sensor_location == 1:
            direction_buffer += 1   #left
        elif sensor_location == 2:
            direction_buffer -= 1   #right

    if not(sensor_buffer[1] or sensor_buffer[2]):
        if direction_buffer >= 3: #should be == 4; somtimes bouncing problems
            rotation_callback(-1)   #left
        elif direction_buffer <= -3: #should be == -4; same as above
            rotation_callback(1)    #right
        print 'direction_buffer was: %r'%direction_buffer
        direction_buffer = 0


class Sensor:
    def __init__(self, sensor_preferences, sensor_location):
        self.pin = sensor_preferences['pin']
        self.sensor_location = sensor_location
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        if sensor_preferences['sensor_type'] == 'nc':
            # 'nc' sensor
            self.normal_status = False
        else:
            # 'no' sensor
            self.normal_status = True

        sensor_buffer[sensor_location] = self.read_sensor()

        if sensor_preferences['bouncetime'] > 0:
            GPIO.add_event_detect(
                self.pin,
                GPIO.BOTH,
                callback=self.callback,
                bouncetime=sensor_preferences['bouncetime']
                )
        else:
            GPIO.add_event_detect(
                self.pin,
                GPIO.BOTH,
                callback=self.callback
                )

    def read_sensor(self):
        if self.normal_status:
            return not(GPIO.input(self.pin))
        else:
            return GPIO.input(self.pin)

    def callback(self, pin):
        sensor_callback(self.read_sensor(), self.sensor_location)


sensor_one = Sensor(rot_sensors['front'], 1)
sensor_two = Sensor(rot_sensors['rear'], 2)
