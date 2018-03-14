import tornado.ioloop
import tornado.web
import requests
import json
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print(self.get_argument("userInfo", ""))
        self.write("Hello, world")

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={jscode}&grant_type=authorization_code'
        finalUrl = url.format(appid='wxef81e23ab76f443e', secret='3b3d5dd92bf6b812d37cc128fc6bd88a', jscode=self.get_argument('code'))
        userInfo = json.loads(self.get_argument('userInfo'))
        res = json.loads(requests.get(finalUrl).text)
        print(res)
        session = DBSession()
        oldUser = session.query(User).filter(User.open_id==res['openid']).first()
        if(oldUser):
            return
        newUser = User(open_id=res['openid'], nick_name=userInfo['nickName'], gender=userInfo['gender'], language=userInfo['language'], city=userInfo['city'], province=userInfo['province'], country=userInfo['country'])
        session.add(newUser)
        session.commit()
        print(newUser.id)
        self.write("Hello, "+self.get_argument('code'))

def make_app():
    settings = {
        "static_path": '/Users/mengwei/git/wechat/niuniu-bill/server/static',
        "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        "login_url": "/login",
        "xsrf_cookies": True,
    }

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()