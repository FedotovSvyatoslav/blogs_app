import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = "category"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    news = orm.relationship("News", secondary="association",
                            back_populates="categories")
