import time


class Pace:
    def __init__(self):
        self.time_buffer = []

    def average_pace(self, offset=3):
        if offset >= len(self.time_buffer):
            offset = len(self.time_buffer) - 1  # 2 records -> 1 pace
        try:
            return ( self.get_pace(offset=offset) / offset )
        except ZeroDivisionError:
            return 0

    def get_pace(self, offset=3):
        try:
            return self.time_buffer[-1] - self.time_buffer[-1 - offset]
        except IndexError:
            return 0

    def turn(self, direction):
        # if direction is 0 rotation_count was set manualy -> reset pace
        if direction < 0:
            self.time_buffer.append(time.time())
        elif direction > 0:
            try:
                self.time_buffer.pop()
            except IndexError:
                pass
        elif direction == 0:
            self.reset()

    def reset(self):
        self.time_buffer[:] = []


if __name__ == "__main__":
    s = Pace()

    for i in range(1000):
        time.sleep(0.001)
        s.turn(-1)

    for i in range(500):
        time.sleep(0.001)
        s.turn(1)
    print(s.average_pace(offset=1200))
