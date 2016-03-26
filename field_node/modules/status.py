import time
from datetime import datetime


class Status:
    def __init__(self, distance_source, pace_source):
        self.distance = distance_source
        self.pace = pace_source
        self.rotation_count = 0
        self.sensors = (0, 0)
        self.rotation_direction = 0
        self.current_layer = self.layer()
        self.current_row = self.row()
        self.reporting = False

    def sensor_update(self, sensor_tuple):
        ''' Updates sensor state. '''
        self.sensors = sensor_tuple
        return(sensor_tuple)

    def rotation_update(self, direction):
        ''' Updates rotation_count, layer and row. '''
        self.rotation_count += direction
        self.rotation_direction = direction
        self.pace.turn(direction)

        _layer = self.current_layer
        self.current_layer = self.layer()
        if self.current_layer != _layer:
            self.layer_update(_layer)

        _row = self.current_row
        self.current_row = self.row()
        if self.current_row != _row:
            self.row_update(_row)
        return(self.rotation_count)

    def rotation_set(self, new_rotation_count):
        ''' Sets rotation_count to 'new_rotation_count', resets pace. '''
        self.rotation_count = new_rotation_count
        self.rotation_update(0)

    def layer_update(self, last):
        print('layer_update')

    def row_update(self, last):
        print('row_update')

    def length_remaining(self):
        ''' Returns remaining cm until rotation_count 0. '''
        return(self.distance.length_remaining(self.rotation_count))

    def length_remaining_m(self):
        ''' Returns float of remaining meters until rotation_count 0. '''
        meters = round(
            float(self.length_remaining()) /
            100.0,
            1)
        return meters

    def time_str(self):
        ''' Returns string of current time. '''
        return time.strftime('%H:%M')

    def time_remaining(self, offset=3):
        ''' Returns remaining time until rotation_count 0. '''
        try:
            return (self.length_remaining() / self.speed_last(offset))
        except ZeroDivisionError:
            return 0

    def time_remaining_str(self, offset=3):
        '''
        Returns string of remaining time until rotation_count is 0.
        Time is calculated from average pace of last 'offset' knobs.
        Format is "(hh)h:mm".
        '''
        ti = int(self.time_remaining(offset)) // 60
        hours = ti // 60
        if hours > 999:
            return '++:++'
        minutes = ti % 60
        return ( str(hours) + ':' + str(minutes).zfill(2) )

    def speed_last_mh(self, offset=1):
        ''' Returns average speed of last 'x' knobs in m/h. '''
        return (round( self.speed_last(offset) * 36, 1))

    def speed_last(self, x):
        ''' Returns average speed of last 'x' knobs in cm/sek. '''
        try:
            return ( self.distance.length(self.rotation_count,
                                          offset=x) /
                     (self.pace.average_pace(offset=x) * x) )
        except ZeroDivisionError:
            return 0

    def layer(self, rot=None):
        '''
        Returns current layer or layer for 'rot' rotation_count if given.
        0 is outer layer.
        '''
        if not(rot):
            rot = self.rotation_count
        return self.distance.layer(rot)

    def layer_hr(self, rot=None):
        '''
        Returns current layer or layer for 'rot' rotation_count if given.
        Starts at 1 for inner layer.
        '''
        if not(rot):
            rot = self.rotation_count
        return self.distance.layer_hr(rot)

    def row(self, rot=None):
        '''
        Returns current row or row for 'rot' rotation_count if given.
        Starting at 0.
        '''
        if not(rot):
            rot = self.rotation_count
        return self.distance.row(rot)

    def rows_max(self):
        ''' Returns list of number of rows per layer ([0] is outer layer) '''
        return self.distance.rows_per_layer

    def set_reel(self, layer, row):
        ''' Sets current reel position to 'row' in 'layer', resets pace. '''
        print('Layer: ', layer, ' - Row: ', row)
        self.rotation_set(self.distance.signals(layer, row))
        # self.current_layer = layer
        # self.current_row = row

    def toggle_report(self):
        self.reporting = not(self.reporting)
        if self.reporting:
            print('Start Reporting')
        else:
            print('Stop Reporting')
        return(self.reporting)

    # following methods may be overwritten by optional modules

    def temperature(self):
        return 0

    def battery_voltage(self):
        return 0
