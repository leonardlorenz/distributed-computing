import sys
import msg_sender
import msg_receiver
from socket import *

DOMAIN = "141.64.167.138"
#DOMAIN = "dbl44.beuth-hochschule.de"
PORT = "44444"
# stop variable, if set to False, program will stop.
STILL_RUNS = True

def main():

    print("connecting to server...")
    CONN = create_connection((DOMAIN, PORT), 5)
    print("joining chat group...")
    
    msg_recv = msg_receiver.msg_receiver(CONN)

    msg_recv.start()

    msg_recv.join()
    
    send_group_join_notify(CONN)
    send_group_notify(CONN)
    print("message sent")
    send_leave_group_notify(CONN)
    print("left group")
    
def send_group_join_notify(CONN):
    # send message of type group join
    message = bytearray(4096)
    message = "dslp/1.1\r\n" + "group join\r\n" + "Freitag-Teams\r\n" + "dslp/end\r\n"
    CONN.sendall(message.encode('utf-8'))

def send_group_notify(CONN):
    # send message of type group notify
    message = bytearray(4096)
    message = "dslp/1.1\r\n" + "group notify\r\n" + "Freitag-Teams\r\n" + "Hallo\nWie gehts\r\n"+ "dslp/end\r\n"
    CONN.sendall(message.encode('utf-8'))

def send_leave_group_notify(CONN):
    # send message of type group leave
    message = "dslp/1.1\r\n" + "group leave\r\n" + "Freitag-Teams\r\n" + "dslp/end\r\n"
    CONN.sendall(message.encode('utf-8'))

if __name__ == '__main__':
    main()

