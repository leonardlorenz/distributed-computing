from threading import Thread
import main
import time
import base64

class msg_sender(Thread):
    def __init__(self, CONN, peer, filename):
        self.CONN = CONN
        self.peer = peer
        Thread.__init__(self)

    def run(self):
        LINE_END = main.LINE_END
        try:
            file_to_send = open(filename, r)
            file_as_text = base64.b64encode(file_to_send.read())
            message = "dslp/1.2" + LINE_END + "peer notify" + LINE_END + peer + LINE_END +
            input() + LINE_END + file_as_text + LINE_END + "dslp/end" + LINE_END
            self.CONN.sendall(message.encode('utf-8'))
        except:
            print("Could not open " + filename + ". Are you sure you have read permissions on this file?")
            main.STILL_RUNS = False

