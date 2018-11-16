from threading import Thread
import main
import time

class msg_sender(Thread):
    def __init__(self, CONN, peer, filename):
        self.CONN = CONN
        self.peer = peer
        Thread.__init__(self)

    def run(self):
        while main.STILL_RUNS:
            message = "dslp/1.2\r\n" + "peer notify\r\n" + peer + "\r\n" + input() + "\r\n" + "dslp/end\r\n"
            self.CONN.sendall(message.encode('utf-8'))
