from socket import *
import base64
import time
import receiver

DOMAIN = "88.198.53.236"
PORT = 80
PEER = "141.64.170.91"
FILENAME = "test.txt"
LINE_END = "\r\n"
IS_RUNNING = True

def main():
    print("--- creating connection")
    CONN = create_connection((DOMAIN, PORT), 3)
    msg_receiver = receiver.receiver(CONN, FILENAME)
    msg_receiver.start()
    print("--- requesting time")
    request_time(CONN)
    time.sleep(1)
    print("--- joining group")
    group_join(CONN)
    time.sleep(1)
    print("--- notifying group")
    group_notify(CONN)
    time.sleep(1)
    print("--- leaving group")
    #group_leave(CONN)
    time.sleep(1)
    print("--- notifying peer")
    peer_notify(CONN)
    while IS_RUNNING:
        time.sleep(1)
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
def group_leave(CONN):
    message = "dslp/1.2" + LINE_END + "group leave" + LINE_END + "Freitag-Teams" + LINE_END + "dslp/end" + LINE_END
    CONN.sendall(message.encode('utf-8'))

if __name__ == "__main__":
    main()
