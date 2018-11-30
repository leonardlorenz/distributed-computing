import socket
import threading
import time

HOST = ""
PORT = 44444
IS_RUNNING = True
GROUPS = []

def main():
    client_response_time(None, None)
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        SOCK.bind((HOST, PORT))
    except socket.error as msg:
        print("Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])
        sys.exit()
    SOCK.listen(10)
    while IS_RUNNING:
        conn, addr = SOCK.accept()
        print("Connected to " + addr[0] + ":" + str(addr[1]))
        threading.Thread(None, listen_for_messages, None, conn, addr)

def listen_for_messages(conn, addr):
    while IS_RUNNING:
        all_data = []
        data = bytearray(8192)
        conn.recv_into(data)
        all_data.append(data)
        all_data_str = ""
        for i in range(0, len(all_data)):
            all_data_str = all_data_str + all_data[i]
        msg_arr = all_data_str.split("\r\n")
        if msg_arr[0] == "dslp/1.2":
            if msg_arr[1] == "request time":
                client_response_time(conn, addr)
            elif msg_arr[1] == "group join":
                client_group_join(msg_arr)
            elif msg_arr[1] == "group leave":
                client_group_leave(conn, addr)
            elif msg_arr[1] == "group notify":
                client_group_notify(conn, addr)
            elif msg_arr[1] == "peer notify":
                client_peer_notify(conn, addr)
            else:
                send_error(conn, addr)

def client_response_time(conn, addr):
    date_time = time.time()
    # yyyy-MM-dd'T'HH:mm:ssX
    date_str = time.strftime("%Y-%m-%dT%H:%M:%S%Z", time.gmtime(date_time))
    message = "dslp/1.2\r\n" + "response time\r\n" + date_str + "\r\n" + "dslp/end\r\n"
    conn.sendall(message.encode("utf-8"))

def client_group_join(msg_arr):
    group_name = msg_arr[2]
    group_exists = False
    group_index = 0
    for i in range(0, len(GROUPS)):
        if GROUPS[i].name == group_name:
            group_exists = True
            group_index = i
    if group_exists:
        GROUPS[group_index].add_member(conn, addr)



def client_group_leave(conn, addr):
    print("")

def client_group_notify(conn, addr):
    print("")

def send_error(conn, addr, error):
    message = "dslp/1.2\r\n" + "error\r\n" + str(error) + "\r\n" + "dslp/end\r\n"
    conn.sendall(message.encode("utf-8"))

if __name__ == "__main__":
    main(conn, addr)
