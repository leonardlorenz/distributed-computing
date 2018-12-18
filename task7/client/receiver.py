from threading import Thread
import socket
import client

class receiver(Thread):
    def __init__(self, CONN):
        self.CONN = CONN
        Thread.__init__(self)

    def run(self):
        conn = self.CONN
        while client.IS_RUNNING:
            packet = self.recv_to_end(self.CONN)
            message = packet.decode('utf-8')
            msg_arr = message.split("\r\n")
            if msg_arr[0] == "dslp/1.2":
                if msg_arr[1] == "group notify":
                    print("(" + msg_arr[2] + ")")
                if msg_arr[1] == "peer notify":
                    # ignore line 2
                    print(msg_arr[3])
                    file_to_write = open(self.filename, "w")
                    file_to_write.write(base64.b64decode(msg_arr[4]).decode("utf-8"))
                if msg_arr[1] == "response time":
                    print("Current server time: " + msg_arr[2])

    def recv_to_end(self, CONN):
        all_data_str = ""
        ended = False
        while not ended:
            data = CONN.recv(4096)
            data_str = data.decode("utf-8")
            protocol_lines = data_str.split("\r\n")
            print(data_str)
            for line in protocol_lines:
                if line == ("dslp/end"):
                    ended = True
                    print("dlsp/end")
