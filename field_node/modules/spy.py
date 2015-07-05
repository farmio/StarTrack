from delegate import Timer
from delegate import Delegate


class Spy:
    def __init__(self, speed, target, spy_prefs):
        self.t_min = target - (target * spy_prefs['accuracy'] / 100.0)
        self.t_max = target + (target * spy_prefs['accuracy'] / 100.0)
        self.speed = speed
        self.speed_spy = Timer(spy_prefs['alert_time'],
                               self.alert,
                               step=spy_prefs['update_time'],
                               update=self.update_speed)
        self.speed_spy.start()
        # self.speed_spy.join()

    def alert(self):
        self.speed_spy.kill()       # or deactivate() ?
        print('ALERT')
        return       # ??

    def update_speed(self):
        v = self.speed()
        print('v:', v, ' min:', self.t_min)
        if self.t_min <= v <= self.t_max:
            print('fits')
            self.speed_spy.reset()
        else:
            print('doesnt fit')

        self.announce(v)

    def announce(self, speed):
        # hook for delegate
        print('announce: ', speed)
        pass


if __name__ == '__main__':
    test_list = [5, 4, 6, 5, 4, 4, 4, 7, 2, 4, 5, 9, 9, 9]

    def test():
        for i in test_list:
            yield i

    test_gen = test()

    def speed():
        for i in test_gen:
            return(i)

    spy = Spy(speed, 5, 20)

    for i in range(5):
        print('main')
        sleep(0.5)
