from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexluceym_secret_key"


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    for n in range(2, 5):
        user = User()
        user.name = f"Пользователь {n}"
        user.about = f"Что то о пользователе {n}"
        user.email = f"user{n}@mail.ru"
        db_sess.add(user)
    db_sess.commit()
    for user in db_sess.query(User).all():
        print(user.name, user.created_date)
    #app.run()


if __name__ == "__main__":
    main()