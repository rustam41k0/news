from typing import Dict, Any
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
from src.db import Base


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    body = Column(String, nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date,
            'body': self.body,
            'deleted': self.deleted,
        }


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, ForeignKey('news.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    comment = Column(String, nullable=False)

