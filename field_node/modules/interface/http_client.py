from time import time, sleep
from threading import Thread
import logging
import requests
import jwt
try:
    import Queue as queue
except ImportError:
    import queue


class Http_Client(object):
    url = ''
    key = ''
    nid = ''
    _last_update = 0

    def __init__(self, server, source, nid):
        Http_Client.url = server.url
        Http_Client.key = server.key
        Http_Client.nid = nid
        Http_Client.source = source

        Http_Client._queue = queue.Queue(maxsize=3)
        Http_Client.thread = Thread(target=Http_Client.__query)
        Http_Client.thread.daemon = True
        Http_Client.thread.start()

    @staticmethod
    def query(payload):
        payload['nid'] = Http_Client.nid
        try:
            Http_Client._queue.put_nowait(payload)
        except queue.Full:
            logging.warning('Request Queue full: %s', payload)

    @staticmethod
    def __query():
        while True:
            payload = Http_Client._queue.get()
            token = jwt.encode(payload, Http_Client.key, algorithm='HS256')
            try:
                r = requests.post(Http_Client.url, data={'jwt': token})
                if r.status_code == '201':
                    logging.info('Req: %s %s', r.status_code, r.reason)
                else:
                    logging.warning('Req: %s %s', r.status_code, r.reason)

            except requests.exceptions.ConnectionError:
                logging.warning('Reconnecting... - Connection Error')
                Http_Client.source.reconnect_umts()
                sleep(45)
                Http_Client._queue.put_nowait(payload)

            except requests.exceptions.RequestException as er:
                logging.warning('Requests Exception: %s', er)
            Http_Client._queue.task_done()

    @staticmethod
    def sign_in():
        payload = {'act': 'start'}
        Http_Client.query(payload)

    @staticmethod
    def sign_out():
        payload = {'act': 'stop'}
        Http_Client.query(payload)

    @staticmethod
    def update():
        payload = {'act': 'push',
                   'rot': Http_Client.source.rotation_count,
                   'spd': Http_Client.source.speed_last_mh(),
                   'row': Http_Client.source.row(),
                   'lay': Http_Client.source.layer_hr(),
                   'rdm': Http_Client.source.length_remaining_m(),
                   'eta': Http_Client.source.time_remaining(),
                   'tmp': Http_Client.source.temperature(),
                   'bat': Http_Client.source.battery_voltage(),
                   'wsp': Http_Client.source.supply_pressure(),
                   'sli': Http_Client.source.light_intensity(),
                   'mws': Http_Client.source.wind_speed()
                   }
        Http_Client.query(payload)

    @staticmethod
    def update_skip(interval=60):
        ''' Update if 'interval' seconds have passed since last call. '''
        if (Http_Client._last_update + interval) <= time():
            Http_Client._last_update = time()
            Http_Client.update()
        else:
            pass
