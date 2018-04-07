import tornado.ioloop
import tornado.web
import requests
import json
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from handlers import index
from handlers import login

engine = create_engine('mysql+mysqlconnector://niuniu-bill:niuniu@localhost:3306/niuniu_bill')

Base = declarative_base()
 
class User(Base):
    __tablename__ = 'user'
 
    id = Column(Integer, primary_key=True)
    open_id = Column(String(45))
    nick_name = Column(String(45))
    gender = Column(Integer)
    language = Column(String(20))
    city = Column(String(45))
    province = Column(String(45))
    country = Column(String(45))

DBSession = sessionmaker(bind=engine)

def make_app():
    settings = {
        "static_path": '/Users/mengwei/git/wechat/niuniu-bill/server/static',
        "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        "login_url": "/login",
        "xsrf_cookies": True,
    }

    return tornado.web.Application([
        (r"/", index.IndexHandler),
        (r"/login", login.LoginHandler),
        (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()