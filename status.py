import time
from datetime import datetime


class Status:
    def __init__(self, position_source, distance_source):
        self.position = position_source
        self.distance = distance_source

    def length_remaining_m(self):
        meters = round(
            float(self.distance.length_remaining(self.position.rotation_count)) /
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
