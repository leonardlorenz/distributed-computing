from threading import Thread
import socket
import client
import base64

class receiver(Thread):
    def __init__(self, CONN, FILENAME):
        self.CONN = CONN
        self.filename = FILENAME
        Thread.__init__(self)

    def run(self):
        conn = self.CONN
        while client.IS_RUNNING:
            data_str = self.recv_to_end(self.CONN)
            msg_arr = data_str.split("\r\n")
            if msg_arr[0] == "dslp/1.2":
                if msg_arr[1] == "group notify":
                    print("(" + msg_arr[2] + ")")
                if msg_arr[1] == "peer notify":
                    print(msg_arr[3])
                    file_to_write = open(self.filename, "w")
                    file_to_write.write(base64.b64decode(msg_arr[4]).decode("utf-8"))
                if msg_arr[1] == "response time":
                    print("Current server time: " + msg_arr[2])

    def recv_to_end(self, CONN):
        ended = False
        all_data_str = ""
        while not ended:
            data = bytearray()
            try:
                data = CONN.recv(4096)
            except:
                #print("No new packages.")
            data_str = data.decode("utf-8")
            all_data_str += data_str
            protocol_lines = data_str.split("\r\n")
            for line in protocol_lines:
                if line == ("dslp/end"):
                    ended = True
                    print("\n\n------------\nreceived message! Message content:\n" + all_data_str + "\n\n")
                    break
            return all_data_str
