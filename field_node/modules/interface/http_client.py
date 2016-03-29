from time import time, strftime
import requests
import jwt


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

    @staticmethod
    def query(payload):
        payload['nid'] = Http_Client.nid,
        token = jwt.encode(payload, Http_Client.key, algorithm='HS256')
        try:
            r = requests.post(Http_Client.url, data={'jwt': token})
            print(strftime("%Y-%m-%d %H:%M:%S"),
                  r.status_code, r.reason)
        except requests.exceptions.RequestException as err:
            print(strftime("%Y-%m-%d %H:%M:%S"), "Requests Exception:", err)

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
        payload = {'rot': Http_Client.source.rotation_count,
                   'spd': Http_Client.source.speed_last_mh(),
                   'row': Http_Client.source.row(),
                   'lay': Http_Client.source.layer_hr(),
                   'rd': Http_Client.source.length_remaining_m(),
                   'eta': Http_Client.source.time_remaining(),
                   'tmp': Http_Client.source.temperature(),
                   'bat': Http_Client.source.battery_voltage()
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
