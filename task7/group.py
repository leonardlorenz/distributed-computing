class group:

    def __init__(self, group_name, group_id):
        self.group_members = []
        self.group_name = group_name
        self.group_id = group_name

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
        for group_member in group_members:
            if group_member["CONN"] == conn and group_member["ADDR"] == addr:
                group_members.remove(group_member)
