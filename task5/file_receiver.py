from threading import Thread
import socket
import main
import base64

class file_receiver(Thread):
    def __init__(self, CONN, filename):
        self.CONN = CONN
        Thread.__init__(self)

    def run(self):
        while main.STILL_RUNS:
            try:
                all_data = []
                while True:
                    data = self.CONN.recv(8192)
                    if not data: break
                    all_data.append(data)
                all_data_str = ''.join(all_data)
                message = all_data_str.decode('utf-8')
                msg_arr = message.split("\r\n")
                if msg_arr[0] == "dslp/1.2":
                    if msg_arr[1] == "peer notify":
                        # ignore line 2
                        print(msg_arr[3])
                        file_to_write = open(filename, w)
                        file_to_write.write(base64.b64decode(msg_arr[4]))
            except socket.timeout:
                continue
