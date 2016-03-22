import RPi.GPIO as GPIO
from threading import Timer


def init_buttons(gpio_pins, btn_cfg):
    bt = btn_cfg['bouncetime']
    buttons = {'enter': Button(gpio_pins['enter'], bounce=bt),
               'esc': Button(gpio_pins['esc'], bounce=bt),
               'plus': Button(gpio_pins['plus'], bounce=bt),
               'minus': Button(gpio_pins['minus'], bounce=bt)}
    return buttons


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
                 hold_delay=1000, hold_repeat=500):
        """
        Repeats `action` afer `hold_delay` every `hold_repeat`
        for as long as button is pushed.
        """
        super(self.__class__, self).__init__(pin, action=action, bounce=bounce)
        self._listen = False
        self.hold_delay = hold_delay / 1000.0
        self.hold_repeat = hold_repeat / 1000.0
        self.hold_timer = None
        self.repeat_timer = None

    def _hold(self):
        if self._listen:
            self._action()
            self.repeat_timer = Resettable_Timer(self.hold_repeat, self._hold)
            self.repeat_timer.start()

    def _callback(self, pin):
        if not(GPIO.input(pin)):
            self._action()
            self._listen = True
            self.hold_timer = Resettrable_Timer(self.hold_delay, self._hold)
            self.hold_timer.start()
        else:
            self._listen = False
            try:
                self.hold_timer.cancel()
                self.repeat_timer.cancel()
            except:
                pass


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
