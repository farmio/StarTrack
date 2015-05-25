#rotation sensor preferences
rot_sensors = {
    ##front sensor
    'front': {
        #GPIO.BCM style pin numeration
        'pin': 24, # 24 -> Pin18
        #sensor contact type - valid are: 'nc' for normally closed type,
        #'no' for normally open  - defaults to 'no'
        'sensor_type': 'no',
        #bounce time for detection in ms
        'bouncetime': 30,
    },
    ##rear sensor
    'rear': {
        #GPIO.BCM style pin numeration
        'pin': 23, # 23 -> Pin17
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
    'windings_outer_layer': 15,
    #dimensions in cm
    'hose_diameter': 8.5,
    #radius of the reel without hose
    'inner_radius': 122.5,
    #distance from center to sensors
    'sensor_radius': 144.5,
}

#lcd preferences
lcd = {
    #display size
    'columns': 20,
    'rows': 4,
    #GPIO.BCM style pin numeration
    'rs': 7,
    'en': 25,
    'd4': 8,
    'd5': 9,
    'd6': 10,
    'd7': 11,
}

#network preferences
net = {
    #sakis3g preferences
    'sakis3g': {
        'arguments': [
            'MODEM=OTHER',
            'OTHER=USBMODEM',
            'USBDRIVER=option',
            #usb id found via lsusb
            'USBMODEM=12d1:1003',
            'APN=CUSTOM_APN',
            'CUSTOM_APN=drei.at',
            #if no user/password is needed use 0
            'APN_USER=0',
            'APN_PASS=0'
        ]
    }
}
