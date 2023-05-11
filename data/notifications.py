import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase

from sqlalchemy import orm


class Notifications(SqlAlchemyBase):
    __tablename__ = "notifications"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    users = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    mister = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=True)
