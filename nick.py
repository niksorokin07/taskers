import sqlite3


class Room:
    def __init__(self, key, managers, users, tasks):
        self.key = key
        self.managers = managers.split(", ")
        self.users = users.split(", ")
        self.tasks = tasks.split(", ")
        self.description = ""

    def add_task(self, task_name):
        self.tasks.append(task_name)

    def delete_task(self, task_name):
        self.tasks.remove(task_name)

    def add_user(self, name):
        self.users.append(name)

    def delete_user(self, name):
        self.users.remove(name)

    def add_manager(self, name):
        self.managers.append(name)

    def delete_manager(self, name):
        self.managers.remove(name)

    def update_desc(self, text):
        self.description = text

    def update(self):
        con = sqlite3.connect("taskerbase.sqlite")
        cur = con.cursor()
        cur.execute(
            f"""UPDATE {self.key}Tasks SET managers = {", ".join(self.managers)}AND users = {", ".join(self.users)} AND
         description = {self.description} AND tasks = {", ".join(self.tasks)}""")
        con.commit()
        con.close()


class User:
    def __init__(self, key, about, email, login, password, rooms, tasks):
        self.key = key
        self.tasks = tasks.split(", ")
        self.about = about
        self.email = email
        self.login = login
        self.password = password
        self.rooms = rooms.split(", ")

    def update_login(self, text):
        self.login = text

    def update_password(self, text):
        self.password = text

    def update_about(self, text):
        self.about = text

    def add_user(self, name):
        self.tasks.append(name)

    def delete_user(self, name):
        self.tasks.remove(name)

    def add_manager(self, name):
        self.rooms.append(name)

    def delete_manager(self, name):
        self.rooms.remove(name)
