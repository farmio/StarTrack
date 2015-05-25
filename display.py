from operator import itemgetter

import Adafruit_CharLCD as AdaLCD


class Display(AdaLCD.Adafruit_CharLCD):
    #spawning two threads updating the display simultaniously couses errors
    def __init__(self, lcd, source):
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
        self.message_buffer = []
        self.init_lcd()

    def update(self):
        for m in sorted(self.message_buffer, key=itemgetter(1,0)):
            print m
            self.set_cursor(m[0], m[1])
            self.message(m[2])
        self.message_buffer = []

    def init_lcd(self):
        self.clear()
        self.message_buffer.append( (0, 0, 'S:') )
        self.message_buffer.append( (0, 1, 'L:') )
        self.message_buffer.append( (8, 1, 'm') )
        self.clock()
        self.update()

    def clock(self):
        self.message_buffer.append( (13, 0, self.source.time_str().rjust(5)) )
        #self.update()

    def rotation_update(self):           #display 2:7, 0; 2:8, 1
        rot_count = self.source.rotation_count()
        rot_dir = self.source.rotation_direction()
        self.message_buffer.append( (2, 0, str(rot_count).rjust(5)) )
        if rot_dir > 0:
            self.message_buffer.append( (8, 0, '<') )
            self.message_buffer.append( (11, 0, ' ') )
        elif rot_dir < 0:
            self.message_buffer.append( (8, 0, ' ') )
            self.message_buffer.append( (11, 0, '>') )
        self.message_buffer.append( (2, 1,
            str(self.source.length_remaining_m()).rjust(6)) )
        self.update()

    def sensor_update(self):    #display 8:11, 0
        sensors = self.source.sensors()
        sensor_message = ''
        for i in sensors:
            sensor_message += '_' if sensors[i] else '-'
        self.message_buffer.append( (9, 0, (str(sensor_message).ljust(2))) )
        self.update()


#display segmentation
#0##3##6##9##2##5##8##
#S:-1234 <--> ti:me Y#
#L:-400.1m           #
#                    #
#                    #
######################
