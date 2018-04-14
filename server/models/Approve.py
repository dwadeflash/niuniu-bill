from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime, Float
from models.base import BaseModel

class Approve(BaseModel):
    __tablename__ = 'approve'
 
    id = Column(Integer, primary_key=True)
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime)
    applicant_id = Column(Integer)
    applicant_name = Column(String(64))
    approver_id = Column(Integer)
    approver_name = Column(String(64))
    status = Column(Integer)
    amount = Column(Float)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    