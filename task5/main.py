import sys
import msg_sender
import msg_receiver
from socket import *

# stop variable, if set to False, program will stop.
STILL_RUNS = True

def main():
    # syntax:
    # make run_receiver filename=foo.txt
    # make run_sender peer=255.255.255.255 filename=foo.txt
    peer = ""
    filename = ""
    if sys.argv[1] == "send":
        if sys.argv[2].startswith("peer"):
            peer = sys.argv[2]
        if sys.argv[3].startswith("filename"):
            filename = sys.argv[3]
        if peer != "" and filename != "":
            print("connecting to server...")
            CONN = connect_to_beuth()
            send = sender.file_sender(connect_to_beuth, peer, filename)
            send.start()

    else if sys.argv[1] == "receive":
        if sys.argv[2].startswith("filename"):
            filename = sys.argv[2]
        if filename != "":
            print("connecting to server...")
            recv = receiver.file_receiver(connect_to_beuth()), filename)
            recv.start()

    recv.join()
    send.join()

    send_leave_group_notify(CONN)
    CONN.close()

def connect_to_beuth():
    DOMAIN = "localhost"
    #DOMAIN = "dbl44.beuth-hochschule.de"
    PORT = "44444"
    CONN = create_connection((DOMAIN, PORT), 5)
    return CONN

def send_group_join_notify(CONN):
    # send message of type group join
    message = bytearray(4096)
    message = "dslp/1.2\r\n" + "group join\r\n" + "Freitag-Teams\r\n" + "dslp/end\r\n"
    CONN.sendall(message.encode('utf-8'))

def send_leave_group_notify(CONN):
    # send message of type group leave
    message = "dslp/1.2\r\n" + "group leave\r\n" + "Freitag-Teams\r\n" + "dslp/end\r\n"
    CONN.sendall(message.encode('utf-8'))

if __name__ == '__main__':
    main()

