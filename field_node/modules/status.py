import time
from datetime import datetime


class Status:
    def __init__(self, position_source, distance_source, pace_source):
        self.position = position_source
        self.distance = distance_source
        self.pace = pace_source

    def length_remaining(self):
        return(self.distance.length_remaining(self.position.rotation_count))

    def length_remaining_m(self):
        meters = round(
            float(self.length_remaining()) /
            100.0,
            1)
        return meters

    def rotation_count(self):
        return self.position.rotation_count

    def sensors(self):
        return self.position.sensor_buffer

    def rotation_direction(self):
        return self.position.last_direction

    def time_str(self):
        return time.strftime('%H:%M')

    def time_remaining(self, offset=3):
        try:
            return (self.length_remaining() / self.speed_last(offset))
        except ZeroDivisionError:
            return 0

    def time_remaining_str(self, offset=3):
        ti = int(self.time_remaining(offset)) / 60
        hours = ti / 60
        if hours > 999:
            return '++:++'
        minutes = ti % 60
        return ( str(hours) + ':' + str(minutes).zfill(2) )

    def speed_last_mh(self, x):
        return (round( self.speed_last(x) * 36 , 1))

    def speed_last(self, x):    #in cm/sek
        try:
            return ( self.distance.length(self.position.rotation_count,
                                                offset=x) /
                           (self.pace.average_pace(offset=x) * x) )
        except ZeroDivisionError:
            return 0

    def layer(self, rot=None):
        if not(rot): rot=self.position.rotation_count
        return self.distance.layer_hr(rot)

    def row(self, rot=None):    #int
        if not(rot): rot=self.position.rotation_count
        return self.distance.row(rot)
