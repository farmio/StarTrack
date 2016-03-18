def display_rotation(*args, **kwargs):
    Queue(display.rotation_update, display_thread, pause=0.01).start()


def display_sensors(*args, **kwargs):
    Queue(display.sensor_update, display_thread, pause=0.01).start()


def attatch_display():
    status.rotation_update += display_rotation
    status.sensor_update += display_sensors
    # status.layer_update += display.layer


def detatch_display():
    status.rotation_update -= display_rotation
    status.sensor_update -= display_sensors

attatch_display()
