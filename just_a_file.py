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
        # здесь будет подключение к базе данных
        pass


class Room_Task(Task):
    def __init__(self, managerkey, user, name, status, description, deadline, date, params):
        super().__init__(name, status, description, deadline, date, params)
        self.managerkey = managerkey
        self.user = user

    def change_user(self, new):
        self.user = new

    def update(self):
        # здесь будет подключение к базе данных
        pass