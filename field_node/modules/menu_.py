from buttons_ import Button
# from buttons import Button_hold





class Sub_Item(object):
    def __init__(self, id):
        self.id = sub_item['id']
        self.show = sub_item['content']


    def escape(self):
        pass

    def enter(self):
        pass

    def plus(self):
        pass

    def minus(self):
        pass

    def show(self):
        pass


def set_hose():
    menu_item = {'id': 1,
                 'caption': 'Set Hose',
                 'content': _content,
                 'enter_btn': _enter,
                 'plus_btn': _plus,
                 'minus_btn': _minus}

    _active = None

    def _content():
        pass

    def _plus():
        _active.plus()


def set_speed():
    pass


def info():
    pass


def exit_menu():
    pass


def start_monitoring():
    pass


def stop_monitoring():
    pass


if __name__ == '__main__':
    from config import Config
    f = file('../config.cfg')
    cfg = Config(f)

    set_buttons(cfg.gpio_pins.buttons)
    try:
        print('Waiting for Interrupt')
        while 1:
            pass
    except KeyboardInterrupt:
        pass
