import socket
import sys
import threading

DOMAIN = "dbl44.beuth-hochschule.de"
PORT = "44444"
PROTOCOLSTART = "dslp/1.1\r\n"
PROTOCOLEND = "dslp/end"

def main():
    if sys.argv[1] == "ascii":
        send_ascii = True
    else:
        send_ascii = False
    CONN = socket.create_connection((DOMAIN, PORT))
    # new thread to receive messages from server
    threading.Thread(None, recv_messages, CONN)
    # join chat group
    send_group_join_notify(CONN)
    send_message(CONN, send_ascii)
    send_leave_group_notify(CONN)
    CONN.close()

def recv_messages(CONN):
    while True:
        packet = CONN.recv()
        message = packet.decode('utf-8')
        msg_arr = message.split("\r\n")
        if msg_arr[0] == "dslp/1.1":
            if msg_arr[1] == "group notify":
                if msg_arr[len(msg_arr) - 1] == "dslp/end":
                    # print every line that is between protocol type
                    # and protocol end
                    for i in range(2, len(msg_arr) - 1):
                        print(msg_arr[i])

def send_group_join_notify(CONN):
    # send message of type group join
    message = bytearray(4096)
    message = (PROTOCOLSTART + "group join\r\n" + PROTOCOLEND).encode('utf-8')
    CONN.sendall(message)

def send_message(CONN, send_ascii):
    # send message of type group join
    if send_ascii == True:
        cli_input = str("\n" +
        "\n░░░░▄▄▄▄▀▀▀▀▀▀▀▀▄▄▄▄▄▄"+
        "\n░░░░█░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░▀▀▄"+
        "\n░░░█░░░▒▒▒▒▒▒░░░░░░░░▒▒▒░░█"+
        "\n░░█░░░░░░▄██▀▄▄░░░░░▄▄▄░░░█"+
        "\n░▀▒▄▄▄▒░█▀▀▀▀▄▄█░░░██▄▄█░░░█"+
        "\n█▒█▒▄░▀▄▄▄▀░░░░░░░░█░░░▒▒▒▒▒█"+
        "\n█▒█░█▀▄▄░░░░░█▀░░░░▀▄░░▄▀▀▀▄▒█"+
        "\n░█▀▄░█▄░█▀▄▄░▀░▀▀░▄▄▀░░░░█░░█"+
        "\n░░█░░▀▄▀█▄▄░█▀▀▀▄▄▄▄▀▀█▀██░█"+
        "\n░░░█░░██░░▀█▄▄▄█▄▄█▄████░█"+
        "\n░░░░█░░░▀▀▄░█░░░█░███████░█"+
        "\n░░░░░▀▄░░░▀▀▄▄▄█▄█▄█▄█▄▀░░█"+
        "\n░░░░░░░▀▄▄░▒▒▒▒░░░░░░░░░░█"+
        "\n░░░░░░░░░░▀▀▄▄░▒▒▒▒▒▒▒▒▒▒░█"+
        "\n░░░░░░░░░░░░░░▀▄▄▄▄▄░░░░░█")
    else:
        cli_input = str(input()):

    message = PROTOCOLSTART + cli_input + "\r\n" + PROTOCOLEND
    CONN.sendall(message.encode('utf-8'))

def send_leave_group_notify(CONN):
    # send message of type group leave
    message = PROTOCOLSTART + "group leave\r\n" + PROTOCOLEND
    CONN.sendall(message.encode('utf-8'))

if __name__ == '__main__':
    main()

