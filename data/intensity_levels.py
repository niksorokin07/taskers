import sqlalchemy
from data.db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('jobs', sqlalchemy.Integer, sqlalchemy.ForeignKey('jobs.id')),
    sqlalchemy.Column('hazard_levels', sqlalchemy.Integer, sqlalchemy.ForeignKey('intensity_level.id'))
)


class IntensityLevel(SqlAlchemyBase):
    __tablename__ = 'intensity_level'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    level = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
