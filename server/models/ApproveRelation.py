from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime, Boolean
from models.base import BaseModel
 
class ApproveRelation(BaseModel):
    __tablename__ = 'approve_relation'
 
    id = Column(Integer, primary_key=True)
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime)
    applicant_id = Column(Integer)
    applicant_name = Column(String(64))
    approver_id = Column(Integer)
    approver_name = Column(String(64))
    enabled = Column(Boolean)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}