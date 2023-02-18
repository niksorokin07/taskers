import datetime
import sqlalchemy
import sqlalchemy.orm as orm

from do_base1.data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    mail = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=False, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tasks = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now, nullable=True)

    pers_tasks = orm.relationship("Pers_task", back_populates="user")

    rooms = orm.relationship("Room", back_populates="users")
