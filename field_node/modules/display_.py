from operator import itemgetter
import RPi.GPIO as GPIO
import Adafruit_CharLCD as AdaLCD


class Display(AdaLCD.Adafruit_CharLCD):
    # spawning two threads updating the display simultaniously couses errors
    def __init__(self, gpio_pins, lcd, source):
        lcd_prefs = [gpio_pins['rs'],
                     gpio_pins['en'],
                     gpio_pins['d4'],
                     gpio_pins['d5'],
                     gpio_pins['d6'],
                     gpio_pins['d7'],
                     lcd['columns'],
                     lcd['rows']]
        AdaLCD.Adafruit_CharLCD.__init__(self, *lcd_prefs)
        self.source = source
        self.message_buffer = []
        self.custom_chars()
        self.init_display()

    def custom_chars(self):
        SYM_LENGTH = [0, 0, 0, 17, 31, 0, 0, 0]
        SYM_LAYER = [8, 8, 20, 20, 10, 9, 4, 2]
        SYM_CLOCK = [0, 14, 21, 23, 17, 14, 0, 0]
        SYM_HOURGLASS = [31, 17, 10, 4, 10, 17, 31, 0]
        SYM_KNOB = [4, 4, 4, 12, 12, 4, 4, 4]
        SYM_CIRCLE = [0, 14, 17, 17, 17, 14, 0, 0]
        SYM_CIRCLE_FULL = [0, 14, 31, 27, 31, 14, 0, 0]
        self.create_char(0, SYM_LENGTH)
        self.create_char(1, SYM_LAYER)
        self.create_char(2, SYM_CLOCK)
        self.create_char(3, SYM_HOURGLASS)
        self.create_char(4, SYM_KNOB)
        self.create_char(5, SYM_CIRCLE)
        self.create_char(6, SYM_CIRCLE_FULL)
        self.sym_length = '\x00'
        self.sym_layer = '\x01'
        self.sym_clock = '\x02'
        self.sym_hourglass = '\x03'
        self.sym_knob = '\x04'
        self.sym_circle = '\x05'
        self.sym_circle_full = '\x06'

    def update(self):
        """ Sort message_buffer and send to display. """
        for m in sorted(self.message_buffer, key=itemgetter(1, 0)):
            print(m)
            self.set_cursor(m[0], m[1])
            self.message(m[2])
        self.message_buffer[:] = []
        self.home()

    def init_display(self):
        self.clear()
        self.message_buffer.append( (0, 0, self.sym_knob) )
        self.message_buffer.append( (0, 1, self.sym_length) )
        self.message_buffer.append( (8, 1, 'm') )
        self.message_buffer.append( (0, 2, self.sym_layer) )
        self.message_buffer.append( (4, 2, '|') )
        self.message_buffer.append( (17, 1, 'm/h') )
        self.message_buffer.append( (12, 2, self.sym_hourglass) )
        self.speed()
        self.layer()
        self.row()
        self.time_remaining()
        self.clock()
        self.update()

    def clock(self):
        self.message_buffer.append( (13, 0, self.source.time_str().rjust(5)) )
        # self.update()

    def rotation_update(self):           # display 2:7, 0; 2:8, 1
        rot_count = self.source.rotation_count
        rot_dir = self.source.rotation_direction
        self.speed()
        # self.row()
        # self.layer()
        self.time_remaining()
        self.clock()
        self.message_buffer.append( (2, 0, str(rot_count).rjust(5)) )
        if rot_dir > 0:
            self.message_buffer.append( (8, 0, '<') )
            self.message_buffer.append( (11, 0, ' ') )
        elif rot_dir < 0:
            self.message_buffer.append( (8, 0, ' ') )
            self.message_buffer.append( (11, 0, '>') )
        self.message_buffer.append(
            (2, 1, str(self.source.length_remaining_m()).rjust(6)) )
        self.update()

    def sensor_update(self):    # display 8:11, 0
        sensors = self.source.sensors
        sensor_message = ''
        for i in sensors:
            sensor_message += self.sym_circle_full if i else self.sym_circle
        self.message_buffer.append( (9, 0, (str(sensor_message).ljust(2))) )
        self.update()

    def layer(self):
        self.message_buffer.append( (2, 2, str(self.source.layer()).rjust(2)) )

    def speed(self):
        speed = self.source.speed_last_mh(offset=3)
        if speed < 1000:
            self.message_buffer.append( (11, 1, str(speed).rjust(5)) )
        else:
            self.message_buffer.append( (11, 1, '>1000') )

    def row(self):
        self.message_buffer.append( (5, 2, str(self.source.row()).ljust(2)) )

    def time_remaining(self):
        timer = self.source.time_remaining_str()
        self.message_buffer.append( (14, 2, timer.rjust(6)) )

# display segmentation
# 0##3##6##9##2##5##8##
# S:-1234 <--> ti:me Y#0
# l:-400.1m  100.3 m/h#1
# L:10|11     T-112:34#2
#                    #3
# #####################

if __name__ == '__main__':
    from config import Config
    from status import Status
    from distance import Distance
    from pace import Pace
    f = file('../config.cfg')
    cfg = Config(f)

    distance = Distance(cfg.reel)
    pace = Pace()
    status = Status(distance, pace)
    display = Display(cfg.gpio_pins.display, cfg.lcd, status)

    try:
        print('Waiting for Interrupt')
        while 1:
            pass
    except KeyboardInterrupt:
        GPIO.cleanup()
