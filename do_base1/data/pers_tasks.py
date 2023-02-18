import datetime
import sqlalchemy
import sqlalchemy.orm as orm

from do_base1.data.db_session import SqlAlchemyBase


class Pers_task(SqlAlchemyBase):
    __tablename__ = 'pers_tasks'

    key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    deadline = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    params = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.key"))
    user = orm.relationship('User')
