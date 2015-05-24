import Adafruit_CharLCD as AdaLCD

from config import lcd


class Display(AdaLCD.Adafruit_CharLCD):
    #spawning two threads updating the display simultaniously couses errors
    def __init__(self, sensor_source):
        lcd_prefs = [lcd['rs'],
                     lcd['en'],
                     lcd['d4'],
                     lcd['d5'],
                     lcd['d6'],
                     lcd['d7'],
                     lcd['columns'],
                     lcd['rows']]
        AdaLCD.Adafruit_CharLCD.__init__(self, *lcd_prefs)
        self.sensor_source = sensor_source
        self.init_lcd()

    def init_lcd(self):
        self.clear()
        self.set_cursor(0, 0)
        self.message('S:')

    def rotation_update(self):           #display 2:7, 0
        rot_count = self.sensor_source.rotation_count
        self.set_cursor(2, 0)
        self.message(str(rot_count).rjust(5))

    def sensor_update(self):    #display 9:10, 0
        sensors = self.sensor_source.sensor_buffer
        self.set_cursor(9, 0)
        sensor_message = ''
        for i in sensors:
            sensor_message += '_' if sensors[i] else '-'
        print 'sensor_message: ', sensor_message
        self.message(str(sensor_message).ljust(2))


#display segmentation
#0##3##6##9##2##5##8##
#S:-1234  <-  ti:me Y#
#                    #
#                    #
#                    #
######################
