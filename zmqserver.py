### ZEROMQ SERVER
import zmq
from threading import Thread
from time import sleep
class zeromq_server(Thread):
    __translation = None
    __rotation = None
    __socket = None
    __message = None
    __isRunning = False
    def __init__(self, Uri):
        context = zmq.Context()
        self.__socket = context.socket(zmq.REP)
        self.__socket.bind(Uri)
        self.__isRunning = True
        Thread.__init__(self)
    def __del__(self):
        self.__socket.close()
    def run(self):
        while self.__isRunning:
            mes = self.__socket.recv().decode("utf-8")
            if(mes == 'OK' and self.__message is not None):
                self.__socket.send_string(self.__message)
            sleep(0.1)
    def set_message(self, message):
        self.__message = message
    def stop_thread(self):
        self.__socket.close()
        self.__isRunning = False;
