from socket import *
import base64
import time
import receiver
import sys

DOMAIN = "141.64.201.154"
#DOMAIN = "88.198.53.236"
PORT = 44444
#PORT = 80
PEER = "141.64.170.91"
KEY = "012345678901234567890123"
FILENAME = "test.txt"
LINE_END = "\r\n"
IS_RUNNING = True

def main():
    print("--- creating connection")
    CONN = create_connection((DOMAIN, PORT), 3)
    # listen for messages
    msg_receiver = receiver.receiver(CONN, FILENAME)
    msg_receiver.start()
    print("--- notifying peer")
    CONN = ""
    peer_notify(CONN)
    while True:
        time.sleep(1)

def peer_notify(CONN):
    global IS_RUNNING
    while IS_RUNNING:
        user_input = input()
        if user_input is "/quit":
            IS_RUNNING = False
        peer = user_input.split(":")[0]
        index_of_split = user_input.find(":")
        message = user_input[index_of_split + 2:]
        packet = "dslp/1.2" + LINE_END + "peer notify" + LINE_END + PEER + LINE_END + message + LINE_END + "dslp/end" + LINE_END
        send_message(CONN, packet)

def send_message(CONN, message):
    try:
        CONN.sendall(message.encode("utf-8"))
    except BrokenPipeError:
        print("Connection with server has broken up.")

if __name__ == "__main__":
    main()
