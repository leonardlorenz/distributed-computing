from socket import *

DOMAIN = "metr1xx.de"
PORT = 44444
PEER = "141.64.167.222"
FILENAME = "test.txt"
LINE_END = "\r\n"

def main():
    CONN = create_connection((DOMAIN, PORT), 5)
    request_time(CONN)
    group_join(CONN)
    notify_group(CONN)
    group_leave(CONN)
    peer_notify(CONN)

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
def leave_group(CONN):
    message = "dslp/1.2" + LINE_END + "group leave" + LINE_END + "Freitag-Teams" + LINE_END + "dslp/end" + LINE_END
    CONN.sendall(message.encode('utf-8'))
