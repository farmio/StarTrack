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

    def sensor_update(self, sensor_tuple):
        self.sensors = sensor_tuple
        return(sensor_tuple)

    def rotation_update(self, direction):
        self.rotation_count += direction
        self.rotation_direction = direction
        self.pace.callback(direction)

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
        self.rotation_count = new_rotation_count
        self.pace.reset()

    def layer_update(self, last):
        print('layer_update')

    def row_update(self, last):
        print('row_update')

    def length_remaining(self):
        return(self.distance.length_remaining(self.rotation_count))

    def length_remaining_m(self):
        meters = round(
            float(self.length_remaining()) /
            100.0,
            1)
        return meters

    def time_str(self):
        return time.strftime('%H:%M')

    def time_remaining(self, offset=3):
        try:
            return (self.length_remaining() / self.speed_last(offset))
        except ZeroDivisionError:
            return 0

    def time_remaining_str(self, offset=3):
        ti = int(self.time_remaining(offset)) // 60
        hours = ti // 60
        if hours > 999:
            return '++:++'
        minutes = ti % 60
        return ( str(hours) + ':' + str(minutes).zfill(2) )

    def speed_last_mh(self, offset=1):
        return (round( self.speed_last(offset) * 36, 1))

    def speed_last(self, x):    # in cm/sek
        try:
            return ( self.distance.length(self.rotation_count,
                                          offset=x) /
                     (self.pace.average_pace(offset=x) * x) )
        except ZeroDivisionError:
            return 0

    def layer(self, rot=None):
        if not(rot):
            rot = self.rotation_count
        return self.distance.layer_hr(rot)

    def row(self, rot=None):    # int
        if not(rot):
            rot = self.rotation_count
        return self.distance.row(rot)
