from threading import Thread
import socket
import main
import base64

class file_receiver(Thread):
    def __init__(self, CONN, filename):
        self.CONN = CONN
        self.filename = filename
        Thread.__init__(self)

    def run(self):
        while main.STILL_RUNS:
            try:
                all_data = []
                data = bytearray(8192)
                self.CONN.recv_into(data)
                all_data.append(data.decode("utf-8"))
                for i in range(0, len(all_data)):
                    all_data_str = "".join(all_data[i])
                all_data_str
                msg_arr = all_data_str.split("\r\n")
                if msg_arr[0] == "dslp/1.2":
                    if msg_arr[1] == "peer notify":
                        # ignore line 2
                        print(msg_arr[3])
                        file_to_write = open(self.filename, "w")
                        file_to_write.write(base64.b64decode(msg_arr[4]).decode("utf-8"))
            except socket.timeout:
                continue
