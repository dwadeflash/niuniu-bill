from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime, Float
from base import Base

class Approve(Base):
    __tablename__ = 'approve'
 
    id = Column(Integer, primary_key=True)
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime)
    applicant_id = Column(Integer)
    approver_id = Column(Integer)
    status = Column(Integer)
    amount = Column(Float)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    