from math import pi


class Hose:
    def __init__(self, reel):
        self.reel = reel
        #layer: inner layer = max_layers -1; outer layer = 0
        #layer_hr: inner layer = 1; outer layer = max_layers
        self.layer_signals = []
        self.sum_signals = []
        self.layer_radius = []
        self.length_per_signal = []
        #self.rows_per_layer = []
        hose_pull_point = round(float(reel['hose_diameter']) / 3,
                                1)

        def get_layer_signals(layer):
            if layer == 0:
                #self.rows_per_layer.append(reel['windings_outer_layer'])
                return reel['windings_outer_layer'] * reel['sensor_targets']
            else:
                #self.rows_per_layer.append(reel['windings_max'])
                return (reel['windings_max'] * reel['sensor_targets'])

        def get_sum_signals(layer, layer_signals):
            if layer == 0:
                return layer_signals
            else:
                return (self.sum_signals[layer - 1] + layer_signals)

        def get_layer_radius(layer):
            return (reel['inner_radius'] +
                    (reel['max_layers'] - (layer + 1)) * reel['hose_diameter'] +
                    hose_pull_point)

        def get_length_per_signal(radius):
            return round((2*radius*pi) / float(reel['sensor_targets']), 2)


        for i in range(reel['max_layers']):
            self.layer_signals.append(get_layer_signals(i))
            self.sum_signals.append(get_sum_signals(i, self.layer_signals[i]))
            self.layer_radius.append(get_layer_radius(i))
            self.length_per_signal.append(
                get_length_per_signal(self.layer_radius[i]))

        print('cm / signal [layer]:  ', self.length_per_signal)
        print('signal/layer [layer]: ', self.layer_signals)
        #print('row / layer [layer]:  ', self.rows_per_layer)

    def layer(self, rotation_count):
        i = 0
        while rotation_count > self.sum_signals[i]:
            i += 1
        else:
            return i

    def layer_hr(self, rotation_count): # _hr -> human readable
        return self.reel['max_layers'] - self.layer(rotation_count)

    def length(self, rotation_count, offset=0):
        return ( self.length_remaining(rotation_count) -
                 self.length_remaining(rotation_count-offset) )

    def length_remaining(self, rotation_count):
        length = 0
        i = 0
        while rotation_count > self.layer_signals[i]:
            length += (self.layer_signals[i] *
                       self.length_per_signal[i])
            rotation_count -= self.layer_signals[i]
            i += 1
        else:
            length += (rotation_count * self.length_per_signal[i])
        return length

    def row(self, rotation_count):
        layer = self.layer(rotation_count)
        count_in_layer = self.sum_signals[layer] - rotation_count
        return count_in_layer // self.reel['sensor_targets']
