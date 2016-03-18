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
        self.columns = lcd['columns']
        self.rows = lcd['rows']
        self.source = source
        self._message_buffer = []
        self._custom_chars()

        # self.show_cursor(True)
        self.clear()
        self.status_3_line()

    def status_3_line(self):
        self.rotation_update = self._status_3_line
        self._status_3_line()

    def status_1_line(self):
        self.rotation_update = self._status_1_line
        self._status_1_line()

    def _status_3_line(self):
        self.clock()
        self.distance()
        self.knob_counter()
        self.layer()
        self.online()
        self.speed()
        self.time_remaining()

        self._update()

    def _status_1_line(self):
        self.clock()
        self.knob_counter()
        self.online()

        self._update()

    def rotation_update(self):
        pass

    def sensor_update(self):    # display 8:11, 0
        sensor_message = ''
        for i in self.source.sensors:
            sensor_message += self.sym_circle_full if i else self.sym_circle
        self._message_buffer.append( (9, 0, (str(sensor_message).ljust(2))) )
        self._update()

    def clock(self):
        self._message_buffer.append( (13, 0, self.source.time_str().rjust(5)) )

    def knob_counter(self):
        rot_count = self.source.rotation_count
        rot_dir = self.source.rotation_direction
        self._message_buffer.append( (0, 0, self.sym_knob + ' ' +
                                     str(rot_count).rjust(5)) )
        if rot_dir > 0:
            self._message_buffer.append( (8, 0, '<') )
            self._message_buffer.append( (11, 0, ' ') )
        elif rot_dir < 0:
            self._message_buffer.append( (8, 0, ' ') )
            self._message_buffer.append( (11, 0, '>') )

    def layer(self):
        m = self.sym_layer + ' '
        m += str(self.source.layer_hr()).rjust(2) + '|'
        m += str(self.source.row()).zfill(2)
        self._message_buffer.append( (0, 1, m) )

    def distance(self):
        self._message_buffer.append(
            (0, 2, self.sym_length +
             str(self.source.length_remaining_m()).rjust(6) + 'm') )

    def speed(self):
        speed = self.source.speed_last_mh(offset=3)
        if speed < 1000:
            self._message_buffer.append( (12, 1, str(speed).rjust(5) + 'm/h') )
        else:
            self._message_buffer.append( (12, 1, '>1000m/h') )

    def time_remaining(self):
        timer = self.source.time_remaining_str()
        self._message_buffer.append( (12, 2,
                                     timer.rjust(6) + ' ' +
                                     self.sym_hourglass) )

    def online(self):
        pass

    def write_row(self, row, message, offset=0, cent=False, prep='', app=''):
        '''
        Writes 'message' to 'row'.
        If 'offset' is set 'message' is prepended with spaces.
        If 'cent' is True 'message' will be centered.
        'prep' gets prepended, 'app' gets appended.
        If 'message' overflows display colums overflow is dropped.
        '''
        message = ' ' * offset + message
        m_chars = self.columns
        if prep:
            m_chars -= len(prep)

        if app:
            m_chars -= len(app)

        if cent:
            message = message[:m_chars].center(m_chars)
        else:
            message = message[:m_chars].ljust(m_chars)

        message = prep + message + app
        self._message_buffer.append( (0, row, message[:self.columns]) )
        self._update()

    def clear_row(self, row):
        spaces = ' ' * self.columns
        self._message_buffer.append( (0, row, spaces) )
        self._update()

    def _custom_chars(self):
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

    def _update(self):
        """ Sort _message_buffer and send to display. """
        for m in sorted(self._message_buffer, key=itemgetter(1, 0)):
            self.set_cursor(m[0], m[1])
            self.message(m[2])
        self._message_buffer[:] = []
        self.home()

# display segmentation
# 0##3##6##9##2##5##8##
# K -1234 <--> ti:me Y#0
# L 10|01     100.3m/h#1
# d-400.1m  -112:34 T#2
#                     #3
# #####################

if __name__ == '__main__':
    from config import Config
    from status import Status
    from distance import Distance
    from pace import Pace
    f = file('../config.cfg')
    cfg = Config(f)

    dist = Distance(cfg.reel)
    pace = Pace()
    status = Status(dist, pace)
    display = Display(cfg.gpio_pins.display, cfg.lcd, status)

    try:
        print('Waiting for Interrupt')
        while 1:
            pass
    except KeyboardInterrupt:
        GPIO.cleanup()
