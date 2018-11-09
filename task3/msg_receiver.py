from threading import Thread
import socket

class msg_receiver(Thread):
    def __init__(self, CONN):
        self.CONN = CONN
        Thread.__init__(self)

    def run(self):
        print("initialized message receiver")
        while True:
            BUFFERSIZE = 64000
            packet = bytearray()
            try:
                packet = self.CONN.recv(BUFFERSIZE)
            except socket.timeout:
                continue
                #print("no new messages")
            message = packet.decode('utf-8')
            msg_arr = message.split("\r\n")
            if msg_arr[0] == "dslp/1.1":
                if msg_arr[1] == "group notify":
                    for msg in msg_arr:
                        fin_msg_arr = msg.split("\n")
                        for i in range(2, len(fin_msg_arr) - 1):
                            print(fin_msg_arr[i])
