class group:

    def __init__(self, group_name):
        self.group_members = []
        self.group_name = group_name

    def add_member(self, conn, addr):
        group_member = {
            "ID"   : str(conn) + str(addr),
            "CONN" : conn,
            "ADDR" : addr
                }
        self.group_members.append(group_member)

    def remove_member(self, conn, addr):
        for member in self.group_members:
            if (str(conn) + str(addr)) in member["ID"]:
                self.group_members.remove(member)

    def notify(self, msg):
        for member in self.group_members:
            conn = member["CONN"]
            addr = member["ADDR"]
            message = ("dslp/1.2\r\n" + "group notify\r\n" + self.group_name + "\r\n" + msg + "\r\n" + "dslp/end\r\n")
            try:
                conn.sendall(message.encode("utf-8"))
            except:
                print("Connection with client " + str(addr) + " broke up.")

    def get_members(self):
        return self.group_members

    def get_group_name(self):
        return self.group_name
