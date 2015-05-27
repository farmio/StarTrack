import RPi.GPIO as GPIO


class Sensor:
    rotation_count = 0
    sensor_buffer = {
        1: False,
        2: False
    }
    direction_buffer = 0
    last_direction = 0

    @classmethod
    def rotation_callback(cls, direction):
        cls.rotation_count += direction
        cls.last_direction = direction
        return direction
        #print('rotation_count: %r'%cls.rotation_count)

    @classmethod
    def sensor_callback(cls, status, sensor_location):
        #print('callback on sensor %r'%sensor_location)
        #print('callback: %r'%status)

        cls.sensor_buffer[sensor_location] = status

        if cls.sensor_buffer[1] == cls.sensor_buffer[2]:
            if sensor_location == 1:
                cls.direction_buffer -= 1   #right
            elif sensor_location == 2:
                cls.direction_buffer += 1   #left
        else:
            if sensor_location == 1:
                cls.direction_buffer += 1   #left
            elif sensor_location == 2:
                cls.direction_buffer -= 1   #right

        if not(cls.sensor_buffer[1] or cls.sensor_buffer[2]):
            if cls.direction_buffer >= 3: #should be == 4; somtimes bouncing problems
                cls.direction_buffer = 0
                cls.rotation_callback(-1)   #left
            elif cls.direction_buffer <= -3: #should be == -4; same as above
                cls.direction_buffer = 0
                cls.rotation_callback(1)    #right
            else:
                #print('direction_buffer was: %r'%cls.direction_buffer)
                cls.direction_buffer = 0

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

        Sensor.sensor_buffer[sensor_location] = self.read_sensor()

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
        Sensor.sensor_callback(self.read_sensor(), self.sensor_location)
