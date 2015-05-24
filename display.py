import Adafruit_CharLCD as AdaLCD

from config import lcd


class Display(AdaLCD.Adafruit_CharLCD):
    #spawning two threads updating the display simultaniously couses errors
        
    def init(self):
        self.clear()
        self.set_cursor(0, 0)
        self.message('S:')

    def rotation_update(self, rot_count):           #display 2:7, 0
        self.set_cursor(2, 0)
        self.message(str(rot_count).rjust(5))

    def sensor_update(self, sensors, direction):    #display 9:10, 0
        self.set_cursor(9, 0)
        sensor_message = ''
        for i in sensors:
            sensor_message += '_' if sensors[i] else '-'
        print 'sensor_message: ', sensor_message
        self.message(str(sensor_message).ljust(2))


display = Display(lcd['rs'],
                  lcd['en'],
                  lcd['d4'],
                  lcd['d5'],
                  lcd['d6'],
                  lcd['d7'],
                  lcd['columns'],
                  lcd['rows']
                  )

#display segmentation
#0##3##6##9##2##5##8##
#S:-1234  <-  ti:me Y#
#                    #
#                    #
#                    #
######################
