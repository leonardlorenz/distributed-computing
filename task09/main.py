#!/bin/python
from socket import *
import sys
import threading

PORT = 80
HTTP_HEADER = "GET / HTTP/1.1\n"

def main():
    DOMAIN = sys.argv[1].split("//")[1].split("/")[0]
    url = sys.argv[1]
    CONN = create_connection((DOMAIN, PORT), 3)
    thread = threading.Thread(None, receive, None, (CONN,))
    thread.start()
    send_get_request(CONN, url, DOMAIN)

def send_get_request(CONN, url, DOMAIN):
    packet = HTTP_HEADER + "Host: " + DOMAIN + "\n"
    print(packet)
    CONN.sendall(packet.encode("ascii"))

def receive(CONN):
    packet_str = recv_to_end(CONN)
    # do stuff with the content depending on the answer code
    print(packet_str.decode("ascii"))

def recv_to_end(CONN):
    try:
        data = bytearray()
        try:
            data = CONN.recv(4096)
        except Exception as e:
            print(e)
        return data
    except BrokenPipeError:
        print("Connection has been closed. Message receiving stopped.")

if __name__ == "__main__":
    main()
