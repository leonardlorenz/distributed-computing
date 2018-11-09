import sys
import msg_sender
import msg_receiver
from socket import *

DOMAIN = "localhost"
#DOMAIN = "dbl44.beuth-hochschule.de"
PORT = "44444"
# stop variable, if set to False, program will stop.
STILL_RUNS = True

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "ascii":
            send_ascii = True
    else:
        send_ascii = False

    print("connecting to server...")
    CONN = create_connection((DOMAIN, PORT), 5)
    print("joining chat group...")
    send_group_join_notify(CONN)

    msg_recv = msg_receiver.msg_receiver(CONN)
    msg_send = msg_sender.msg_sender(CONN,send_ascii)

    msg_recv.start()
    print("listening for messages...")
    msg_send.start()
    print("Send a message!")

    msg_recv.join()
    msg_send.join()

    send_leave_group_notify(CONN)
    CONN.close()

def send_group_join_notify(CONN):
    # send message of type group join
    message = bytearray(4096)
    message = "dslp/1.1\r\n" + "group join\r\n" + "Freitag-Teams\r\n" + "dslp/end\r\n"
    CONN.sendall(message.encode('utf-8'))

def send_leave_group_notify(CONN):
    # send message of type group leave
    message = "dslp/1.1\r\n" + "group leave\r\n" + "Freitag-Teams\r\n" + "dslp/end\r\n"
    CONN.sendall(message.encode('utf-8'))

if __name__ == '__main__':
    main()

