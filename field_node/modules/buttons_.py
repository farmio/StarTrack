# import RPi.GPIO as GPIO
from threading import Timer


class Button(object):
    """ Button class for pushbuttons attatched to RPi.GPIO. """
    def __init__(self, pin, action=None, bounce=30):
        """
        Button on GPIO-Pin `pin` triggers `action` function (defaults to pass).
        `bounce` sets software debouncing time in ms.
        """
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
        if not(pin):
            self._action()


if __name__ == '__main__':
    def y():
        print('set')

    def set_action():
        plus_button.set_action(y)

    def plus_action():
        print('plus')

    def minus_action():
        plus_button.del_action()

    def enter_action():
        plus_button.set_action(plus_action)

    def do_nothing():
        pass

    plus_button = Button(14, action=plus_action)
    minus_button = Button_hold(15, action=minus_action)
    b = Button(17, action=set_action)
    c = Button(27, action=enter_action)

    try:
        print('Waiting for Interrupt')
        while 1:
            pass
    except KeyboardInterrupt:
        GPIO.cleanup()
