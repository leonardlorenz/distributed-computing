class group:

    def __init__(self, group_name, group_id):
        self.group_members = []
        self.group_name = group_name

    def __init__(self, group_name, group_id, group_members):
        self.group_members = []
        self.group_name = group_name
        self.group_id = group_name
        self.group_members = group_members

    def add_member(self, conn, addr):
        group_member = {
            "ID"   : str(conn) + str(addr)
            "CONN" : conn
            "ADDR" : addr
                }
        self.group_members.append(group_member)

    def remove_member(self, conn, addr):
        for i in range(0, len(group_members)):
            if (str(conn) + str(addr)) in group_members[i]["ID"]:
                group_members.remove(group_members[i])

    def notify(msg):
        for i in range(0, len(group_members)):
            conn = group_members[i]["CONN"]
            addr = group_members[i]["ADDR"]
            conn.sendall(message = "dslp/1.2\r\n" + "group notify\r\n" + self.group_name + "\r\n" + msg + "\r\n" + "dslp/end\r\n")

    def get_members():
        return self.group_members
