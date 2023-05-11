import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase

from sqlalchemy import orm


class Jobs(SqlAlchemyBase):
    __tablename__ = "jobs"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=True)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Integer, default=False)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, nullable=True)
    #user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship("User")
    intensity_level = orm.relationship("IntensityLevel", secondary="association",  backref="jobs")
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
