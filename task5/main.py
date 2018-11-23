import sys
import file_sender
import file_receiver
from socket import *

# stop variable, if set to False, program will stop.
STILL_RUNS = True
LINE_END = "\r\n"

def main():
    # syntax:
    # make run_receiver filename=foo.txt
    # make run_sender peer=255.255.255.255 filename=foo.txt
    peer = ""
    filename = ""
    threads = []
    if sys.argv[1] == "send":
        peer = sys.argv[2]
        filename = sys.argv[3]
        if peer != "" and filename != "":
            print("connecting to server...")
            CONN = connect_to_beuth()
            send = file_sender.file_sender(CONN, peer, filename)
            send.start()
            send.join()
            CONN.close()

    elif sys.argv[1] == "receive":
        filename = sys.argv[2]
        if filename != "":
            print("connecting to server...")
            CONN = connect_to_beuth()
            recv = file_receiver.file_receiver(CONN, filename)
            recv.start()
            recv.join()
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
    message = "dslp/1.2" + LINE_END + "group join" + LINE_END + "Freitag-Teams" + LINE_END + "dslp/end" + LINE_END
    CONN.sendall(message.encode('utf-8'))

def send_leave_group_notify(CONN):
    # send message of type group leave
    message = "dslp/1.2" + LINE_END + "group leave" + LINE_END + "Freitag-Teams" + LINE_END + "dslp/end" + LINE_END
    CONN.sendall(message.encode('utf-8'))

if __name__ == '__main__':
    main()

