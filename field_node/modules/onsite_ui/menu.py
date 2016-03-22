
def init_menu(display, buttons, status):
    Menu(display, buttons, status)
    s = Set_Hose('Set Hose')
    t = Toggle_Report('Report')


class Menu(object):
    ''' Menu class for single-line LCD controlled by 4 buttons. '''
    disp_row = 3
    items = []
    current_item = 0
    disp = None
    btn = None
    status = None

    def __init__(self, display, buttons, status):
        Menu.disp = display
        Menu.btn = buttons
        Menu.status = status
        Menu.exit_menu()

    @staticmethod
    def show_menu():
        Menu.btn['esc'].set_action(Menu.exit_menu)
        Menu.btn['plus'].set_action(Menu.next_item)
        Menu.btn['minus'].set_action(Menu.prev_item)
        Menu.item_switch()

    @staticmethod
    def item_switch():
        Menu.btn['enter'].set_action(Menu.items[Menu.current_item].select)
        Menu.items[Menu.current_item].switch_to()

    @staticmethod
    def next_item():
        Menu.current_item = (Menu.current_item + 1) % len(Menu.items)
        Menu.item_switch()

    @staticmethod
    def prev_item():
        Menu.current_item = (Menu.current_item - 1) % len(Menu.items)
        Menu.item_switch()

    @staticmethod
    def select_item():
        Menu.btn['esc'].set_action(Menu.show_menu)
        Menu.btn['enter'].set_action(Menu.items[Menu.current_item].enter)
        Menu.btn['plus'].set_action(Menu.items[Menu.current_item].plus)
        Menu.btn['minus'].set_action(Menu.items[Menu.current_item].minus)

    @staticmethod
    def exit_menu():
        Menu.disp.clear_row(Menu.disp_row)
        Menu.current_item = 0
        Menu.btn['enter'].set_action(Menu.show_menu)
        Menu.btn['esc'].del_action()
        Menu.btn['plus'].del_action()
        Menu.btn['minus'].del_action()

    @staticmethod
    def write(*args, **kwargs):
        Menu.disp.write_row(Menu.disp_row, *args, **kwargs)


class Item(Menu):
    def __init__(self, caption):
        type(self).items.append(self)
        self.caption = caption

    def switch_to(self):
        ''' Called when Menu toggles to this Item. '''
        type(self).write(self.caption, cent=True, prep='<', app='>')

    def select(self):
        ''' Called when Item is picked. '''
        type(self).select_item()

    def enter(self):
        ''' Function for Button 'enter' while Item is active. '''
        type(self).exit_menu()

    def plus(self):
        ''' Function for Button 'plus' while Item is active. '''
        pass

    def minus(self):
        ''' Function for Button 'minus' while Item is active. '''
        pass


class Set_Hose(Item):
    def select(self):
        self.active = 0
        self.cursor = None
        self.layer = type(self).status.layer()
        self.row = type(self).status.row()
        self.max_rows = type(self).status.rows_max()
        self.max_layers = len(self.max_rows)
        super(Set_Hose, self).select()
        self._update()

    def enter(self):
        if self.active == 0:
            self.active = 1
            self._update()
        else:
            type(self).status.set_reel(self.layer, self.row)
            super(Set_Hose, self).exit_menu()

    def plus(self):
        if self.active == 0:
            self.layer = (self.layer + 1) % self.max_layers
        else:
            self.row = (self.row - 1) % self.max_rows[self.layer]
        self._update()

    def minus(self):
        if self.active == 0:
            self.layer = (self.layer - 1) % self.max_layers
        else:
            self.row = (self.row + 1) % self.max_rows[self.layer]
        self._update()

    def _update(self):
        if self.active == 0:
            message = 'Layer: '
            message += str(self.max_layers - self.layer).rjust(2)
        else:
            message = 'Row:   '
            message += str(self.max_layers - self.layer).rjust(2) + '|'
            message += str(self.row).zfill(2)
        type(self).write(message)


class Toggle_Report(Item):
    def __init__(self, caption):
        self._caption = caption
        super(Toggle_Report, self).__init__(caption)

    def switch_to(self):
        ''' Called when Menu toggles to this Item. '''
        if self.status.reporting:
            caption_ = 'Stop '
        else:
            caption_ = 'Start '
        self.caption = caption_ + self._caption
        super(Toggle_Report, self).switch_to()

    def select(self):
        ''' Called when Item is picked. '''
        type(self).write(self.caption + ' ?')
        super(Toggle_Report, self).select()

    def enter(self):
        ''' Function for Button 'enter' while Item is active. '''
        type(self).status.toggle_report()
        super(Toggle_Report, self).exit_menu()
