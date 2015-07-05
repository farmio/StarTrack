import RPi.GPIO as GPIO


class Rotation(object):
    sensor_buffer = {
        1: False,
        2: False
    }
    direction_buffer = 0
    last_direction = 0

    @classmethod
    def signal(cls, direction):
        # hook for delegate
        return (direction)

    @classmethod
    def sensor_signal(cls, status, sensor_location):
        cls.sensor_buffer[sensor_location] = status

        if cls.sensor_buffer[1] == cls.sensor_buffer[2]:
            if sensor_location == 1:
                cls.direction_buffer -= 1   # right
            elif sensor_location == 2:
                cls.direction_buffer += 1   # left
        else:
            if sensor_location == 1:
                cls.direction_buffer += 1   # left
            elif sensor_location == 2:
                cls.direction_buffer -= 1   # right

        if not(cls.sensor_buffer[1] or cls.sensor_buffer[2]):
            if cls.direction_buffer >= 3:  # not == 4; because bouncing problem
                cls.direction_buffer = 0
                cls.signal(-1)   # left
            elif cls.direction_buffer <= -3:  # should be == -4; same as above
                cls.direction_buffer = 0
                cls.signal(1)    # right
            else:
                # print('direction_buffer was: %r'%cls.direction_buffer)
                cls.direction_buffer = 0

        return( (cls.sensor_buffer[1], cls.sensor_buffer[2]) )


class Sensor(Rotation):
    def __init__(self, sensor_preferences, sensor_location):
        self.pin = sensor_preferences['pin']
        self.sensor_location = sensor_location
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        if sensor_preferences['sensor_type'] == 'nc':
            # 'nc' sensor
            self.normal_status = False
        else:
            # 'no' sensor
            self.normal_status = True

        super(Sensor, self).sensor_buffer[sensor_location] = self.read_sensor()

        if sensor_preferences['bouncetime'] > 0:
            GPIO.add_event_detect(
                self.pin,
                GPIO.BOTH,
                callback=self._callback,
                bouncetime=sensor_preferences['bouncetime']
            )
        else:
            GPIO.add_event_detect(
                self.pin,
                GPIO.BOTH,
                callback=self._callback
            )

    def read_sensor(self):
        if self.normal_status:
            return not(GPIO.input(self.pin))
        else:
            return GPIO.input(self.pin)

    def _callback(self, pin):
        super(Sensor, self).sensor_signal(self.read_sensor(),
                                          self.sensor_location)
