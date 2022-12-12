import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Videos(SqlAlchemyBase):
    __tablename__ = 'videos'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    video_name = sqlalchemy.Column(sqlalchemy.Text)
    video_path = sqlalchemy.Column(sqlalchemy.Text)
    count_view = sqlalchemy.Column(sqlalchemy.Integer)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
