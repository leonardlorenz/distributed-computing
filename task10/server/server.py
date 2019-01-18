import socket
import threading
import time
import group
import sys

HOST = str(socket.gethostbyname(socket.gethostname()))
PORT = 44444
IS_RUNNING = True
GROUPS = []
KNOWN_CLIENTS = []

def main():
    print("initializing socket")
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("trying to bind")
    try:
        SOCK.bind((HOST, PORT))
        print("bound!")
    except Exception as msg:
        print("Please run this server as root.")
        print("Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])
        SOCK.close()
        sys.exit()
    print("listening")
    SOCK.listen(10)
    while IS_RUNNING:
        conn, addr = SOCK.accept()
        print("Connected to " + addr[0] + ":" + str(addr[1]))
        client = {
                "ADDR" : addr,
                "CONN" : conn
                }
        KNOWN_CLIENTS.append(client)
        thread = threading.Thread(None, listen_for_messages, None, (client,))
        thread.start()

def listen_for_messages(client):
    try:
        conn = client["CONN"]
        addr = client["ADDR"]
        while IS_RUNNING:
            data_str = recv_to_end(conn)
            msg_arr = data_str.split("\r\n")
            if msg_arr[0] == "dslp/1.2":
                if msg_arr[1] == "request time":
                    print("--- request time")
                    client_response_time(client)
                elif msg_arr[1] == "group join":
                    client_group_join(msg_arr[2], client)
                    print("--- " + str(client["ADDR"]) + " group join " + msg_arr[2])
                elif msg_arr[1] == "group leave":
                    client_group_leave(msg_arr[2], client)
                    print("--- " + str(client["ADDR"]) + " group leave " + msg_arr[2])
                elif msg_arr[1] == "group notify":
                    client_group_notify(msg_arr[2], msg_arr[3], client)
                    print("--- " + str(client["ADDR"]) + " group notify " + msg_arr[2])
                elif msg_arr[1] == "peer notify":
                    client_peer_notify(msg_arr[2], msg_arr[3], client)
                    print("--- " + str(client["ADDR"]) + " peer notify " + msg_arr[2])
                else:
                    send_error("Not a valid message type.", client)
            else:
                send_error("Invalid Protocol. Protocol used: " + msg_arr[0], client)
    # connection with client broke up
    except BrokenPipeError as msg:
        client["CONN"].close()
        # remove clients from known clients
        for known_client in KNOWN_CLIENTS:
            if client["ADDR"] == known_client["ADDR"]:
                KNOWN_CLIENTS.remove(client)
        # remove client from groups
        for group in GROUPS:
            group.remove_member(client["CONN"], client["ADDR"])
        # kill client thread
        print("client " + str(client["ADDR"]) + " disconnected.")
        sys.exit()

def recv_to_end(CONN):
    ended = False
    all_data_str = ""
    while not ended:
        data = bytearray()
        try:
            data = CONN.recv(4096)
        except:
            continue
            #print("No new packages.")
        data_str = data.decode("utf-8")
        all_data_str += data_str
        protocol_lines = data_str.split("\r\n")
        for line in protocol_lines:
            if line == ("dslp/end"):
                ended = True
                break
        return all_data_str

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
    group_is_member = False
    group_index = 0
    for group_i in GROUPS:
        if group_name == group_i.get_group_name():
            group_exists = True
            for member in group_i.get_members():
                if conn == member["CONN"]:
                    group_is_member = True
                    break
            if group_is_member == False:
                group_i.add_member(conn, addr)
                break
    if not group_exists:
        new_group = group.group(group_name)
        new_group.add_member(conn, addr)
        GROUPS.append(new_group)
    if group_is_member:
        message = "User is already member of this group. You can't join a group that you're already a member of."
        send_error(message, client)

"""
if the group exists,
the client is known,
the client is member of the group,
notify all other clients of this group with the message attached
"""
def client_group_leave(group_name, client):
    conn = client["CONN"]
    addr = client["ADDR"]
    group_exists = False
    group_is_member = False
    group_index = 0
    for group_i in GROUPS:
        if group_name == group_i.get_group_name():
            group_exists = True
            for member in group_i.get_members():
                if conn == member["CONN"]:
                    group_is_member = True
                    group_i.remove_member(conn, addr)
                    break
    if not group_exists:
        message = "The specified group doesn't exist."
        send_error(message, client)
    if not group_is_member:
        message = "User is not member of the specified group. You can't leave a group that you're not a member of."
        send_error(message, client)

"""
if the client is member of the group,
notify all other clients of this group with the message attached
"""
def client_group_notify(group_name, msg, client):
    conn = client["CONN"]
    addr = client["ADDR"]
    group_exists = False
    group_is_member = False
    for group_i in GROUPS:

        if group_name == group_i.get_group_name():
            group_exists = True
            for member in group_i.get_members():
                if conn == member["CONN"]:
                    print("-|- user is member of the group!")
                    group_is_member = True
                    group_i.notify(msg)
    if not group_exists:
        message = "The specified group doesn't exist"
        send_error(message, client)
    if not group_is_member:
        message = "User is not member of the specified group. You can't send a message to a group that you're not a member of."
        send_error(message, client)

def client_peer_notify(peer, msg, client):
    conn = client["CONN"]
    addr = client["ADDR"]
    client_is_known = False
    IS_RUNNING = False
    for client_i in KNOWN_CLIENTS:
        if addr == client_i["ADDR"]:
            client_is_known = True
            message = "dslp/1.2\r\n" + "peer notify\r\n" + peer + "\r\n" + msg + "\r\n" + "dslp/end\r\n"
            client_i["CONN"].sendall(message.encode("utf-8"))
    if not client_is_known:
        message = "The peer you're trying to send a message to has not connected to the server yet."
        send_error(message, client)

def send_error(error, client):
    conn = client["CONN"]
    addr = client["ADDR"]
    message = "dslp/1.2\r\n" + "error\r\n" + str(error) + "\r\n" + "dslp/end\r\n"
    conn.sendall(message.encode("utf-8"))

if __name__ == "__main__":
    main()
