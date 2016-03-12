
class Menu(object):
    items = []
    current_item = 0

    @classmethod
    def next_item(cls):
        print('len: ', len(cls.items))
        print('item:', cls.current_item)
        if (cls.current_item + 1) < len(cls.items):
            cls.current_item += 1
        else:
            cls.current_item = 0
        cls.items[cls.current_item].switch_to()

    @classmethod
    def first_item(cls):
        cls.current_item = 0
        cls.items[0].switch_to()

    @classmethod
    def add_item(cls, item):
        cls.items.append(item)


class Item(Menu):
    def __init__(self, set_buttons):
        super(self.__class__, self).add_item(self)
        self.set_buttons = set_buttons

    def switch_to(self):
        self.set_buttons()
        self.set_display()

    def set_buttons(self):
        pass

    def set_display(self):
        pass

# set_length = Item()
