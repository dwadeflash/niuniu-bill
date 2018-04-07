from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JsonBase:
    def to_dict(self):
        res = []
        for item in self.__dict__:
            if isinstance(self.__dict__[item], Column):
                res.append(item)