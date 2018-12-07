import socket
import threading
import time

HOST = ""
PORT = 44444
IS_RUNNING = True
GROUPS = []
KNOWN_CLIENTS = []

def main():
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
        client = {
                "ADDR"    : addr
                "CONN"  : conn
                }
        KNOWN_CLIENTS.append(client)
        threading.Thread(None, listen_for_messages, None, conn, addr)

def listen_for_messages(client):
    conn = client["CONN"]
    addr = client["ADDR"]
    while IS_RUNNING:
        all_data = []
        data = bytearray(8192)
        try:
            conn.recv_into(data)
            all_data.append(data)
            all_data_str = ""
            for i in range(0, len(all_data)):
                all_data_str = all_data_str + all_data[i]
            msg_arr = all_data_str.split("\r\n")
            if msg_arr[0] == "dslp/1.2":
                if msg_arr[1] == "request time":
                    client_response_time(client)
                elif msg_arr[1] == "group join":
                    client_group_join(msg_arr[2], client)
                elif msg_arr[1] == "group leave":
                    client_group_leave(msg_arr[2], client)
                elif msg_arr[1] == "group notify":
                    client_group_notify(msg_arr[2], msg_arr[3], msg_arr[4], client)
                elif msg_arr[1] == "peer notify":
                    client_peer_notify(client)
                else:
                    send_error(client)
        except:
            KNOWN_CLIENTS.remove(client)

def client_response_time(client):
    conn = client["CONN"]
    addr = client["ADDR"]
    date_time = time.time()
    # yyyy-MM-dd'T'HH:mm:ssX
    date_str = time.strftime("%Y-%m-%dT%H:%M:%S%Z", time.gmtime(date_time))
    message = "dslp/1.2\r\n" + "response time\r\n" + date_str + "\r\n" + "dslp/end\r\n"
    conn.sendall(message.encode("utf-8"))

def client_group_join(group_name, client):
    conn = client["CONN"]
    addr = client["ADDR"]
    group_exists = False
    group_index = 0
    for i in range(0, len(GROUPS):
        if group_name in GROUPS[i]["NAME"]
            group_exists = True
            GROUPS[i].add_member(conn, addr)
    if not group_exists:
        new_group = group.group(group_name)
        new_group.add_member(conn, addr)
        GROUPS.append(new_group)

def client_group_leave(group_name, client):
    conn = client["CONN"]
    addr = client["ADDR"]
    group_exists = False
    group_is_member = False
    group_index = 0
    for i in range(0, len(GROUPS):
        if group_name in GROUPS[i]["NAME"]
            group_exists = True
            if (str(conn) + str(addr)) in GROUPS[i].get_members()["ID"]
                group_is_member = True
                GROUPS[i].remove_member(conn, addr)
    if not group_exists:
        message = "dslp/1.2\r\n" + "error\r\n" + "The specified group doesn't exist.\r\n" + "dslp/end\r\n"
        send_error(conn, addr, error)
    if not group_is_member:
        message = "dslp/1.2\r\n" + "error\r\n" + "User is not member of the specified group. You can't leave a group that you're not a member of.\r\n" + "dslp/end\r\n"
        send_error(conn, addr, error)

def client_group_notify(group_name, msg, client):
    conn = client["CONN"]
    addr = client["ADDR"]
    group_exists = False
    group_is_member = False
    group_index = 0
    for i in range(0, len(GROUPS)):
        if group_name in GROUPS[i]["NAME"]
            group_exists = True
            if (str(conn) + str(addr)) in GROUPS[i].get_members()["ID"]
                group_is_member = True
                GROUPS[i].notify(msg)
    if not group_exists:
        message = "dslp/1.2\r\n" + "error\r\n" + "The specified group doesn't exist.\r\n" + "dslp/end\r\n"
        send_error(conn, addr, error)
    if not group_is_member:
        message = "dslp/1.2\r\n" + "error\r\n" + "User is not member of the specified group. You can't send a message to a group that you're not a member of.\r\n" + "dslp/end\r\n"
        send_error(conn, addr, error)

def client_peer_notify(peer, msg, file_str, client):
    conn = client["CONN"]
    addr = client["ADDR"]
    for i in range(0, len(KNOWN_CLIENTS))
        if addr == KNOWN_CLIENTS[i]["ADDR"]
            message = "dslp/1.2\r\n" + "peer notify\r\n" + peer + "\r\n" + msg + "\r\n" + file_str + "\r\n" + "dslp/end\r\n"
            KNOWN_CLIENTS[i]["CONN"].sendall(message.encode("UTF-8"))

def send_error(conn, addr, error):
    message = "dslp/1.2\r\n" + "error\r\n" + str(error) + "\r\n" + "dslp/end\r\n"
    conn.sendall(message.encode("utf-8"))

if __name__ == "__main__":
    main(conn, addr)
