from subprocess32 import *

from config import net


class Sakis3g:
    connect_call = ['sakis3g', 'connect'] + net['sakis3g']['arguments']
    disconnect_call = ['sakis3g', 'disconnect']

    @staticmethod
    def connect():
        try:
            output = check_output(connect_call)
            print 'output : ', output
        except CalledProcessError:
            print 'output error : ', output

    @staticmethod
    def disconnect():
        try:
            output = check_output(disconnect_call)
            print 'output : ', output
        except CalledProcessError:
            print 'output error : ', output


class Network:
    def __init__():
        pass

    @staticmethod
    def connect():
        pass


Sakis3g.connect()
