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


def rotation_callback(status, sensor_location):
    print('callback on sensor %r'%sensor_location)
    print('callback: %r'%status)

    global rotation_count
    global direction_buffer

    sensor_buffer[sensor_location] = status

    if sensor_buffer[1] == sensor_buffer[2]:
        if sensor_location == 1:
            print 'right'
            direction_buffer -= 1
        elif sensor_location == 2:
            print 'left'
            direction_buffer += 1
    else:
        if sensor_location == 1:
            print 'left'
            direction_buffer += 1
        elif sensor_location == 2:
            print 'right'
            direction_buffer -= 1

    if not(sensor_buffer[1] or sensor_buffer[2]):
        print 'sensoren frei!'
        if direction_buffer >= 3: #should be == 4; somtimes bouncing problems
            print '1/38 Runde nach links'
            rotation_count -= 1
        elif direction_buffer <= -3: #should be == -4; same as above
            print '1/38 Runde nach rechts'
            rotation_count += 1
        print direction_buffer
        direction_buffer = 0
        print rotation_count


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
        rotation_callback(self.read_sensor(), self.sensor_location)


sensor_one = Sensor(rot_sensors['front'], 1)
sensor_two = Sensor(rot_sensors['rear'], 2)


try:
    print 'Waiting for Interrupt'
    while 1:
        pass
        
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
