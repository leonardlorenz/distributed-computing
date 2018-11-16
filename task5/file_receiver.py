from threading import Thread
import socket
import main

class file_receiver(Thread):
    def __init__(self, CONN):
        self.CONN = CONN
        Thread.__init__(self)

    def run(self):
        while True:
            if main.STILL_RUNS == False:
                break
            else:
                try:
                    packet = self.CONN.recv()
                    message = packet.decode('utf-8')
                    msg_arr = message.split("\r\n")
                    if msg_arr[0] == "dslp/1.2":
                        if msg_arr[1] == "peer notify":
                            # everything from the line after group notify
                            # to the line before protocol ender
                            for i in range(3, len(msg_arr) - 2):
                                print("(" + msg_arr[2] + ") " + msg_arr[i])
                except socket.timeout:
                    continue
