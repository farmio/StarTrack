from config import reel

def get_distance(rotation_count):
    distance = 0

class Layers:
    def __init__(self):
        self.sum_signals = []

        def signals_per_layer(layer):
            if layer == 0:
                return reel['windings_outer_layer'] * reel['sensor_targets']
            else:
                return (reel['windings_max'] * reel['sensor_targets'] +
                        self.sum_signals[layer - 1])

        for i in range(reel['max_layers']):
            self.sum_signals.append(signals_per_layer(i))

    def current(self, rotation_count):
        i = 0
        while rotation_count > self.sum_signals[i]:
            i += 1
        else:
            return i

    def current_hr(self, rotation_count): # _hr -> human readable
        return reel['max_layers'] - self.current(rotation_count)


layer = Layers()
print len(layer.sum_signals)
print layer.current(300)
print layer.current(700)
