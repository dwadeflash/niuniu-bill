from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from tornado.options import options
import redis

engine = create_engine(options.databaseUrl)

DBSession = sessionmaker(bind=engine)
session = DBSession()

r = redis.StrictRedis(host=options.redishost, port=options.redisport, db=0)