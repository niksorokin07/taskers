class Authorization():
    def __init__(self, base):
        self.base = {'names': [], 'mails': [], 'logins': [],
                     'passwords': []}  # словарь, где в будущем будут храниться данные из БД

    def registr(self, name, mail, login, password):
        if mail in self.base['mails']:
            return 'Пользователь с такой почтой уже зарегистрирован!'
        if login in self.base['logins']:
            return 'Пользователь с таким логином уже зарегистрирован!'
        self.base['names'].append(name)
        self.base['mails'].append(mail)
        self.base['logins'].append(login)
        self.base['passwords'].append(password)
        return True

    def log_in(self, login, password):
        if (login not in self.base['logins']) or (password not in self.base['passwords']) or (
                self.base['logins'].index(login) != self.base['passwords'].index(password)):
            return 'Неверный логин или пароль'
        return True
