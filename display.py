import Adafruit_CharLCD as AdaLCD

from config import lcd


class Display(AdaLCD.Adafruit_CharLCD):
    #spawning two threads updating the display simultaniously couses errors
    def __init__(self, source):
        lcd_prefs = [lcd['rs'],
                     lcd['en'],
                     lcd['d4'],
                     lcd['d5'],
                     lcd['d6'],
                     lcd['d7'],
                     lcd['columns'],
                     lcd['rows']]
        AdaLCD.Adafruit_CharLCD.__init__(self, *lcd_prefs)
        self.source = source
        self.init_lcd()

    def init_lcd(self):
        self.clear()
        self.set_cursor(0, 0)
        self.message('S:')
        self.update_time()
        self.set_cursor(0, 1)
        self.message('L:')
        self.set_cursor(8, 1)
        self.message('m')

    def update_time(self):
        self.set_cursor(13, 0)
        self.message(self.source.time_str().rjust(5))

    def rotation_update(self):           #display 2:7, 0; 2:8, 1
        rot_count = self.source.rotation_count()
        rot_dir = self.source.rotation_direction()
        self.set_cursor(2, 0)
        self.message(str(rot_count).rjust(5))
        if rot_dir > 0:
            self.set_cursor(8, 0)
            self.message('<')
            self.set_cursor(11, 0)
            self.message(' ')
        elif rot_dir < 0:
            self.set_cursor(8, 0)
            self.message(' ')
            self.set_cursor(11, 0)
            self.message('>')
        self.set_cursor(2, 1)
        self.message(str(self.source.length_remaining_m()).rjust(6))

    def sensor_update(self):    #display 8:11, 0
        sensors = self.source.sensors()
        self.set_cursor(9, 0)
        sensor_message = ''
        for i in sensors:
            sensor_message += '_' if sensors[i] else '-'
        self.message(str(sensor_message).ljust(2))
        print sensor_message



#display segmentation
#0##3##6##9##2##5##8##
#S:-1234 <--> ti:me Y#
#L:-400.1m           #
#                    #
#                    #
######################
