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


class Proximity_Sensor(Rotation):
    def __init__(self, gpio_pin, sensor_preferences, sensor_location):
        self.pin = gpio_pin
        self.sensor_location = sensor_location
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        if sensor_preferences['sensor_type'] == 'nc':
            # 'nc' sensor
            self.normal_status = False
        else:
            # 'no' sensor
            self.normal_status = True

        super(Proximity_Sensor, self).sensor_buffer[sensor_location] = self.get_state()

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

    def get_state(self):
        if self.normal_status:
            return not(GPIO.input(self.pin))
        else:
            return GPIO.input(self.pin)

    def _callback(self, pin):
        super(Proximity_Sensor, self).sensor_signal(
            self.get_state(),
            self.sensor_location)


if __name__ == '__main__':
    from config import Config
    f = file('../config.cfg')
    cfg = Config(f)

    # Proximity Sensors need 2nd argument 1 or 2
    sensor_one = Proximity_Sensor(cfg.gpio_pins.sensors['front'],
                                  cfg.rot_sensors,
                                  1)
    sensor_two = Proximity_Sensor(cfg.gpio_pins.sensors['rear'],
                                  cfg.rot_sensors,
                                  2)

    try:
        print('Waiting for Interrupt')
        while 1:
            pass
    except KeyboardInterrupt:
        GPIO.cleanup()
