import sys
from msg_sender import msg_sender
from msg_receiver import msg_receiver
from socket import *

#DOMAIN = "localhost"
DOMAIN = "dbl44.beuth-hochschule.de"
PORT = "44444"
PROTOCOLSTART = "dslp/1.1\r\n"
PROTOCOLEND = "dslp/end\r\n"

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
    # stop variable, if set to False, program will stop.
    print("listening for messages...")

    msg_recv = msg_receiver(CONN)
    msg_send = msg_sender(CONN,send_ascii)

    msg_send.start()
    msg_recv.start()

    msg_recv.join()
    msg_send.join()

    send_leave_group_notify(CONN)
    CONN.close()

def send_group_join_notify(CONN):
    # send message of type group join
    message = bytearray(4096)
    message = (PROTOCOLSTART + "group join\r\n" + "Freitag-Teams\r\n" + PROTOCOLEND).encode('utf-8')
    CONN.sendall(message)

def send_leave_group_notify(CONN):
    # send message of type group leave
    message = PROTOCOLSTART + "group leave\r\n" + PROTOCOLEND
    CONN.sendall(message.encode('utf-8'))

if __name__ == '__main__':
    main()

