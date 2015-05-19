#rotation sensor preferences

rot_sensors = {
    ##front sensor
    'front': {
        #GPIO.BCM style pin numeration
        'pin': 8, # 8 -> Pin24
        #sensor contact type - valid are: 'nc' for normally closed type,
        #'no' for normally open  - defaults to 'no'
        'sensor_type': 'no',
        #bounce time for detection in ms
        'bouncetime': 30,
    },
    ##rear sensor
    'rear': {
        #GPIO.BCM style pin numeration
        'pin': 7, # 7 -> Pin26
        #sensor contact type - valid are: 'nc' for normally closed type,
        #'no' for normally open - defaults to 'no'
        'sensor_type': 'no',
        #bounce time for detection in ms
        'bouncetime': 30
    }
}

#reel dimensions
reel = {
    #sensor targets per revolution
    'sensor_targets': 38,
    #maximum hose layers
    'max_layers': 3,
    #windings per layer
    'windings_max': 17,
    #windings outer layer
    'windings_outer_layer': 10,
    #dimensions in cm
    'hose_diameter': 8.5,
    #radius of the reel without hose
    'inner_radius': 122.5,
    #distance from center to sensors
    'sensor_radius': 144.5,
}
