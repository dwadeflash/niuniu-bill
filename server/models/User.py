from sqlalchemy import Column, String, Integer, create_engine
from models.base import BaseModel

class User(BaseModel):
    __tablename__ = 'user'
 
    id = Column(Integer, primary_key=True)
    open_id = Column(String(45))
    nick_name = Column(String(45))
    gender = Column(Integer)
    language = Column(String(20))
    city = Column(String(45))
    province = Column(String(45))
    country = Column(String(45))

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}