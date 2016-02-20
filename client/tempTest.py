import requests
import jwt  # pip install PyJWT
from w1thermsensor import W1ThermSensor
from threading import Thread
from time import sleep
from time import strftime


def readTemp():
    sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18S20)
    temp = sensor.get_temperature()
    return(temp)


def sendTemp():
    url = 'http://startrack.farmous.net/post.php'
    temp = readTemp()
    payload = {'temp': temp}
    token = jwt.encode(payload, 'example_key', algorithm='HS256')
    try:
        r = requests.post(url, data={'jwt': token})
        print(strftime("%Y-%m-%d %H:%M:%S"),
              r.status_code, r.reason, temp)
    except requests.exceptions.RequestException as err:
        print(strftime("%Y-%m-%d %H:%M:%S"), "Requests Exception:", err)


class InfiniteTimer(Thread):
    """ Infinite timer class. `Timer()` spawns a new thread. """
    def __init__(self, delay, func):
        """
        `func(self)` is called every `delay` seconds
        Start with self.start()
        """
        self.delay = delay
        self.func = func
        self.stop = False
        Thread.__init__(self)
        self.setDaemon(True)

    def kill(self):
        """ Stops timer - ends thread before next update. """
        self.stop = True

    def run(self):
        while True:
            if self.stop:
                return
            else:
                self.func()
                sleep(self.delay)


asdf = InfiniteTimer(30, sendTemp)

asdf.start()

try:
    print('Waiting for Interrupt')
    while 1:
        pass
except KeyboardInterrupt:
    print('Good bye!')
