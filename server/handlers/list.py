# coding:utf-8

from handlers.base import BaseHandler
from models.Approve import Approve
from models.ApproveRequest import ApproveRequest
from dao.base import session
from util.cjson import CJsonEncoder

import logging
logger = logging.getLogger('boilerplate.' + __name__)

import requests
import json
from tornado.web import authenticated
import time

class ListHandler(BaseHandler):
    # @authenticated
    def get(self):
        userId = self.get_current_user_id()
        list = []
        try:
            type = int(self.get_argument('type'))
            if type == 1:
                # 我提交的
                list = session.query(Approve).filter(Approve.applicant_id==userId).all()
            elif type == 2:
                # 待审批的
                list = session.query(Approve).filter(Approve.approver_id==userId).all()
            data = []
            for item in list:
                data.append(item.to_dict())
            res = {'success': True, 'data': json.dumps(data, cls=CJsonEncoder)}
        except Exception as e:
            print e
            res = {'success': False}
            res['errorMsg'] = str(e)
        self.write(res)