from flask import Flask
from do_base.data import db_session
from do_base.data.users import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexluceym_secret_key"


def main():
    db_session.global_init("db/taskerbase.db")
    db_sess = db_session.create_session()
    for n in range(2, 5):
        user = User()
        user.login = f"Логин {n}"
        user.password = f"123_{n}"
        user.about = f"Что то о пользователе {n}"
        user.mail = f"user{n}@mail.ru"
        db_sess.add(user)
    db_sess.commit()
    for user in db_sess.query(User).all():
        print(user.login, user.password)
    app.run()


if __name__ == "__main__":
    main()