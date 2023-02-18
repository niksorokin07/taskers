import datetime
import sqlalchemy

from do_base1.data.db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class Room(SqlAlchemyBase):
    __tablename__ = 'rooms'

    key = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    managers = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tasks = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    room_tasks = orm.relationship("Room_task", back_populates="room")

    room_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.key"))
    users = orm.relationship('User', back_populates="rooms")
