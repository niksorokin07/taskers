from flask import Flask
from do_base1.data import db_session
from do_base1.data.rooms import Room
from do_base1.data.room_tasks import Room_task
from do_base1.data.users import User
from do_base1.data.pers_tasks import Pers_task

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexluceym_secret_key"


def main():
    db_session.global_init("do_base1/db/taskerbase.db")
    db_sess = db_session.create_session()
    for n in range(1, 5):
        user = User()
        user.login = f"Логин {n}"
        user.password = f"123_{n}"
        user.about = f"Что то о пользователе {n}"
        user.mail = f"user{n}@mail.ru"
        pers_task = Pers_task(name=f"Имя перс. задачи {n}", status=f"Статус {n}")
        db_sess.add(user)
        db_sess.add(pers_task)
        user.pers_tasks.append(pers_task)
        room = Room()
        room.name = f"Имя комнаты {n}"
        room_task = Room_task(manager=f"Менеджер комнаты {n}", name=f"Комнатная задача 1", status=f"Статус задачи")
        db_sess.add(room)
        db_sess.add(room_task)
        room.room_tasks.append(room_task)
        user.rooms.append(room)
    db_sess.commit()
    for user in db_sess.query(User).all():
        print(user.login, user.password, user.pers_tasks[0].name, user.rooms[0].name)
    for room in db_sess.query(Room).all():
        print(room.name, room.room_tasks[0].name, room.room_tasks[0].manager, room.users.login)
    app.run()


if __name__ == "__main__":
    main()