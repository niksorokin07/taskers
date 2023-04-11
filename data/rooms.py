import datetime
import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Room(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "rooms"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=True)
    tasks = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('jobs.id'), nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)