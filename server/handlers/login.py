from handlers.base import BaseHandler
from models.User import User
from dao.base import session

import logging
logger = logging.getLogger('boilerplate.' + __name__)

import requests
import json
from sqlalchemy import Column, String, Integer

class LoginHandler(BaseHandler):
    def get(self):
        user = self.login()
        self.write(user)
        self.set_secure_session(user['sessionId'], json.dumps(user))

    def post(self):
        user = self.login()
        self.set_secure_session(user['sessionId'], json.dumps(user))

    def login(self):
        user = self.get_current_user()
        if user:
            return user
        try:
            url = 'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={jscode}&grant_type=authorization_code'
            finalUrl = url.format(appid='wxef81e23ab76f443e', secret='3b3d5dd92bf6b812d37cc128fc6bd88a', jscode=self.get_argument('code'))
            userInfo = json.loads(self.get_argument('userInfo'))
            res = json.loads(requests.get(finalUrl).text)
            print(res)
            oldUser = session.query(User).filter(User.open_id==res['openid']).first()
            loginUser = res
            if(oldUser):
                print('old user login')
                loginUser['id'] = oldUser.id
                loginUser['nickName'] = oldUser.nick_name
                loginUser['sessionId'] = self.generateSessionId()
                return loginUser
            newUser = User(open_id=res['openid'], nick_name=userInfo['nickName'], gender=userInfo['gender'], language=userInfo['language'], city=userInfo['city'], province=userInfo['province'], country=userInfo['country'])
            session.add(newUser)
            session.commit()
            print(newUser.id)
            loginUser['id'] = newUser.id
            loginUser['nickName'] = newUser.nick_name
            loginUser['sessionId'] = self.generateSessionId()
            return loginUser
        except Exception as e:
            print(e)
            raise e
