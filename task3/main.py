import socket
import sys
import threading

DOMAIN = "dbl44.beuth-hochschule.de"
PORT = "44444"
PROTOCOLSTART = "dslp/1.1\r\n"
PROTOCOLEND = "dslp/end"
SOCK = None
CONN = None

def main():
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CONN = socket.create_connection((DOMAIN, PORT))
    # new thread to receive messages from server
    threading.Thread(None, recv_messages)
    # join chat group
    send_group_join_notify()
    send_message()
    send_leave_group_notify()
    SOCK.close()

def recv_messages():
    while True:
        message = SOCK.recv()
        msg_arr = message.split("\r\n")
        if msg_arr[0] == "dslp/1.1":
            if msg_arr[1] == "group notify":
                # print every line that is between protocol type
                # and protocol end
                for i in range(2, len(msg_arr) - 1):
                    print(msg_arr[i])

def send_group_join_notify():
    # send message of type group join
    message = PROTOCOLSTART + "group join\r\n" + PROTOCOLEND
    SOCK.sendall(message.encode('utf-8'))

def send_message():
    # send message of type group join
    message = PROTOCOLSTART + str(raw_input()) + "\r\n" + PROTOCOLEND
    SOCK.sendall(message.encode('utf-8'))

def send_leave_group_notify():
    # send message of type group leave
    message = PROTOCOLSTART + "group leave\r\n" + PROTOCOLEND
    SOCK.sendall(message.encode('utf-8'))

if __name__ == '__main__':
    main()

