from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime
from base import Base

class ApproveRecord(Base):
    __tablename__ = 'approve_record'
 
    id = Column(Integer, primary_key=True)
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime)
    approve_request_id = Column(Integer)
    status = Column(Integer)
    memo = Column(String(256))

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

