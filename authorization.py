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


class PasswordError(Exception):
    pass


class LengthError(PasswordError):
    pass


class LetterError(PasswordError):
    pass


class DigitError(PasswordError):
    pass


class SequenceError(PasswordError):
    pass


keyboard = ('йцукенгшщзхъ', 'фывапролджэё', 'ячсмитьбю', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm')


def check_password(password):
    try:
        if len(password) <= 8:
            raise LengthError
        flag_lower = False
        flag_upper = False
        flag_digit = False
        for elem in password:
            if elem.isalpha():
                if elem.islower():
                    flag_lower = True
                else:
                    flag_upper = True
            elif elem.isdigit():
                flag_digit = True
        if not flag_lower or not flag_upper:
            raise LetterError
        if not flag_digit:
            raise DigitError
        for i in range(len(password) - 2):
            for j in range(len(keyboard)):
                if password[i:i + 3].lower() in keyboard[j]:
                    raise SequenceError
        return 'ok'
    except LengthError:
        return 'Длина пароля должна быть больше 8 симловов!'
    except LetterError:
        return 'В пароле должны быть символы разного регистра!'
    except DigitError:
        return 'В пароле должна быть хотя бы одна цифра!'
    except SequenceError:
        return 'В пароле не должно быть ни одной комбинации из 3 буквенных символов, стоящих рядом в строке клавиатуры!'

