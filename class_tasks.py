import sqlite3


class Task:
    def __init__(self, name, status, description, deadline, date, params):
        self.name = name
        self.status = status
        self.description = description
        self.deadline = deadline
        self.date = date
        self.params = params

    def update_name(self, new):
        self.name = new

    def update_status(self, new):
        self.status = new

    def update_description(self, new):
        self.description = new

    def update_deadline(self, new):
        self.deadline = new

    def update_date(self, new):
        self.date = new

    def update_params(self, new):
        self.params = new


class Personal_Task(Task):
    def __init__(self, userkey, name, status, description, deadline, date, params):
        super().__init__(name, status, description, deadline, date, params)
        self.userkey = userkey

    def update(self):
        con = sqlite3.connect("taskerbase.sqlite")
        cur = con.cursor()
        cur.execute(f"""UPDATE {self.userkey}Tasks SET name = {self.name}AND status = {self.status} AND
         description = {self.description} AND deadline = {self.deadline} AND date = {self.date} AND
         {self.params} = params""")
        con.commit()
        con.close()


class Room_Task(Task):
    def __init__(self, roomkey, manager, user, name, status, description, deadline, date, params):
        super().__init__(name, status, description, deadline, date, params)
        self.roomkey = roomkey
        self.manager = manager
        self.user = user

    def change_user(self, new):
        self.user = new

    def update(self):
        con = sqlite3.connect("taskerbase.sqlite")
        cur = con.cursor()
        cur.execute(f"""UPDATE {self.roomkey}Tasks SET manager = {self.manager} AND user = {self.user} AND 
        name = {self.name}AND status = {self.status} AND description = {self.description} AND 
        deadline = {self.deadline} AND date = {self.date} AND {self.params} = params""")
        con.commit()
        con.close()
        