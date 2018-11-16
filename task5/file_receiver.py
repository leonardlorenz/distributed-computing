from threading import Thread
import socket
import main

class msg_receiver(Thread):
    def __init__(self, CONN):
        self.CONN = CONN
        Thread.__init__(self)

    def run(self):
        while True:
            if main.STILL_RUNS == False:
                break
            else:
                BUFFERSIZE = 64000
                packet = bytearray(BUFFERSIZE)
                try:
                    packet = self.CONN.recv(BUFFERSIZE)
                except socket.timeout:
                    continue
                message = packet.decode('utf-8')
                msg_arr = message.split("\r\n")
                if msg_arr[0] == "dslp/1.1":
                    if msg_arr[1] == "group notify":
                        # everything from the line after group notify
                        # to the line before protocol ender
                        print(msg_arr[2])
                        Base64.decode(msg_arr[3])
