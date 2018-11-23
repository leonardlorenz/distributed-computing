from threading import Thread
import main
import time
import base64

class file_sender(Thread):
    def __init__(self, CONN, peer, filename):
        self.CONN = CONN
        self.peer = peer
        self.filename = filename
        Thread.__init__(self)

    def run(self):
        LINE_END = main.LINE_END
        try:
            file_to_send = open(self.filename, "r")
            text = file_to_send.read()
            file_as_text = base64.b64encode(text.encode('utf-8'))
            user_input = input()
            message = "dslp/1.2" + LINE_END + "peer notify" + LINE_END + self.peer + LINE_END + user_input + LINE_END + file_as_text.decode("utf-8") + LINE_END + "dslp/end" + LINE_END
            print("message created")
            self.CONN.sendall(message.encode('utf-8'))
            print("message sent")
        except IOError:
            print("Could not open " + self.filename + ". Are you sure you have read permissions on this file?")
            main.STILL_RUNS = False

