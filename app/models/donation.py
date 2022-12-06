from sqlalchemy import Column, ForeignKey, Integer, Text

from .basemodel import BaseModel


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
