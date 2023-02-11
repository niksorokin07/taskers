import datetime
import sqlalchemy

from do_base.data.db_session import SqlAlchemyBase


class Room_task(SqlAlchemyBase):
    __tablename__ = 'room_tasks'

    key = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    # manager - тот, кто создал задачу и может её редактировать
    manager = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                             default=datetime.datetime.now)
    deadline = sqlalchemy.Column(sqlalchemy.DateTime,
                             default=datetime.datetime.now)
    params = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # user - тот, кто выполняет задачу
    # user_id = sqlalchemy.Column(sqlalchemy.Integer,
                               # sqlalchemy.ForeignKey("users.key"))
    # user = orm.relationship('User')