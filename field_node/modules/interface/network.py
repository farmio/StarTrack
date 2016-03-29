from threading import Thread
try:
    import subprocess32 as subprocess
    import Queue as queue
except ImportError:
    import subprocess
    import queue


class UMTS(object):
    path = 'sakis3g'
    args = []
    _busy = False
    connect_callback = None
    disconnect_callback = None
    status_callback = None

    def __init__(self, config):
        UMTS.sakis_path = config['path']
        UMTS.args[:] = config['arguments']

        UMTS._queue = queue.Queue(maxsize=1)
        UMTS.thread = Thread(target=UMTS.__worker)
        UMTS.thread.daemon = True
        UMTS.thread.start()

    @staticmethod
    def set_callbacks(status):
        UMTS.connect_callback = status.umts_connected
        UMTS.disconnect_callback = status.umts_disconnected
        UMTS.status_callback = status.umts_status_update

    @staticmethod
    def connect():
        arguments = ['connect'] + UMTS.args
        callback = UMTS.connect_callback
        print 'Connecting...'
        UMTS._do(arguments, callback)

    @staticmethod
    def disconnect():
        arguments = ['disconnect']
        callback = UMTS.disconnect_callback
        print 'Disconnecting...'
        UMTS._do(arguments, callback)

    @staticmethod
    def status():
        ''' Calls callback(0) if connected; callback(6) if not connected. '''
        arguments = ['status']
        callback = UMTS.status_callback
        print 'Checking connection status...'
        UMTS._do(arguments, callback)

    @staticmethod
    def _do(arguments, callback):
        try:
            if not UMTS._busy:
                UMTS._queue.put_nowait((arguments, callback))
            else:
                print 'Busy'
                raise queue.Full
        except queue.Full:
            print 'UMTS Queue Full'
            if callable(callback):
                callback(-1)

    @staticmethod
    def __worker():
        while True:
            arguments, callback = UMTS._queue.get()
            UMTS._busy = True
            try:
                returncode = subprocess.call([UMTS.sakis_path] + arguments)
                if callable(callback):
                    callback(returncode)
            except OSError:
                print('maybe trying to execute a non-existent file:',
                      UMTS.sakis_path)
            UMTS._queue.task_done()
            UMTS._busy = False

if __name__ == '__main__':
    from time import sleep
    args = {'path': 'echo', 'arguments': 'asdf'}
    a = UMTS(args)
    a.connect()
    a.disconnect()
    a.status()
    try:
        print('Waiting for Interrupt')
        while 1:
            sleep(1)
            print 'waiting'
    except KeyboardInterrupt:
        pass
