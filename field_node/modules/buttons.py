import RPi.GPIO as GPIO
from threading import Timer


class Button(object):
    """ Button class for pushbuttons attatched to RPi.GPIO. """
    def __init__(self, pin, action=None, bounce=30):
        """
        Button on GPIO-Pin `pin` triggers `action` function (defaults to pass).
        `bounce` sets software debouncing time in ms.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            pin,
            GPIO.BOTH,
            callback=self._callback,
            bouncetime=bounce
        )
        if action:
            self.set_action(action)

    def set_action(self, action):
        """ Replaces action triggered by button with `action` function. """
        self._action = action

    def del_action(self):
        """ Removes action triggered by button. """
        def nothing():
            pass

        self._action = nothing

    def _action(self):
        pass

    def _callback(self, pin):
        if not(GPIO.input(pin)):
            self._action()


class Button_hold(Button):
    """ Button class that additionally repeats triggered action. """
    def __init__(self, pin, action=None, bounce=30,
                 hold_time=1000, hold_repeat=500):
        """
        Repeats `action` afer `hold_time` every `hold_repeat`
        for as long as button is pushed.
        """
        super(self.__class__, self).__init__(pin, action=action, bounce=bounce)
        self._listen = False
        self.hold_time = hold_time / 1000.0
        self.hold_repeat = hold_repeat / 1000.0
        self.hold_timer = None

    def _hold(self):
        if self._listen:
            self._action()
            self.repeat_timer = Timer(self.hold_repeat, self._hold)
            self.repeat_timer.start()

    def _callback(self, pin):
        if not(GPIO.input(pin)):
            self._action()
            self._listen = True
            self.hold_timer = Timer(self.hold_time, self._hold)
            self.hold_timer.start()
        else:
            self._listen = False
            self.hold_timer.cancel()


def set_action():
    pass


def plus_action():
    print('plus')


def minus_action():
    print('minus')


def enter_action():
    pass


def do_nothing():
    pass

if __name__ == '__main__':
    plus_button = Button(14)
    minus_button = Button_hold(15)

    try:
        print('Waiting for Interrupt')
        while 1:
            pass
    except KeyboardInterrupt:
        GPIO.cleanup()
