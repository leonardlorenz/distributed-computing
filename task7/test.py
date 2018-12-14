from socket import *
import base64
import time

DOMAIN = "88.198.53.236"
PORT = 80
PEER = "141.64.167.222"
FILENAME = "test.txt"
LINE_END = "\r\n"

def main():
    print("creating connection")
    CONN = create_connection((DOMAIN, PORT), 3)
    print("requesting time")
    request_time(CONN)
    print("joining group")
    group_join(CONN)
    print("notifying group")
    group_notify(CONN)
    print("leaving group")
    group_leave(CONN)
    print("notifying peer")
    peer_notify(CONN)
    CONN.close()

def peer_notify(CONN):
    file_as_text = bytearray()
    try:
        file_to_send = open(FILENAME, "r")
        text = file_to_send.read()
        file_as_text = base64.b64encode(text.encode('utf-8'))
    except IOError:
        print("Could not open " + FILENAME + ". Are you sure you have read permissions on this file?")
    user_input = "hellow peer"
    message = "dslp/1.2" + LINE_END + "peer notify" + LINE_END + PEER + LINE_END + user_input + LINE_END + file_as_text.decode("utf-8") + LINE_END + "dslp/end" + LINE_END
    CONN.sendall(message.encode('utf-8'))
    print("message sent")

# request server time
def request_time(CONN):
    message = "dslp/1.2" + LINE_END + "request time" + LINE_END + "dslp/end" + LINE_END
    CONN.sendall(message.encode('utf-8'))
    data = bytearray(8192)
    CONN.recv_into(data)
    data_str = data.decode("utf-8").split("\r\n")
    if data_str[1] == "response time":
        print("Current server time: " + data_str[2])

# send message of type group join
def group_join(CONN):
    message = "dslp/1.2" + LINE_END + "group join" + LINE_END + "Freitag-Teams" + LINE_END + "dslp/end" + LINE_END
    CONN.sendall(message.encode('utf-8'))

# send message to group
def group_notify(CONN):
    msg = "hellow"
    message = "dslp/1.2" + LINE_END + "group notify" + LINE_END + "Freitag-Teams" + LINE_END + msg + LINE_END + "dslp/end" + LINE_END
    CONN.sendall(message.encode('utf-8'))

# send message of type group leave
def group_leave(CONN):
    message = "dslp/1.2" + LINE_END + "group leave" + LINE_END + "Freitag-Teams" + LINE_END + "dslp/end" + LINE_END
    CONN.sendall(message.encode('utf-8'))

if __name__ == "__main__":
    main()
