import datetime
import sqlalchemy

from do_base.data.db_session import SqlAlchemyBase


class Room(SqlAlchemyBase):
    __tablename__ = 'rooms'

    key = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    managers = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    # user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                # sqlalchemy.ForeignKey("users.key"))
    # user = orm.relationship('User')
