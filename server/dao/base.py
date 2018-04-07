from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from tornado.options import options

engine = create_engine(options.databaseUrl)

DBSession = sessionmaker(bind=engine)
session = DBSession()