# coding:utf-8

from handlers.base import BaseHandler
from models.Approve import Approve
from models.ApproveRequest import ApproveRequest
from models.ApproveRelation import ApproveRelation
from dao.base import session

import logging
logger = logging.getLogger('boilerplate.' + __name__)

import requests
import json
from tornado.web import authenticated
import time
from sqlalchemy import *

class CreateHandler(BaseHandler):
    @authenticated
    def post(self):
        userId = self.get_current_user_id()
        userName = self.get_current_user_name()
        relation = session.query(ApproveRelation).filter(and_(ApproveRelation.applicant_id == userId, ApproveRelation.approver_id.isnot(None))).first()
        if not relation:
            res = {'success': False}
            res['errorMsg'] = '尚未绑定好友关系，无法提交！'
            res['errorCode'] = 'FRIEND_RELATION_UNBUNDED'
            self.write(res)
            return
        try:
            param = self.request.body.decode('utf-8')
            param = json.loads(param)
            now = time.localtime()
            relation = session.query(ApproveRelation).filter(ApproveRelation.applicant_id == userId).first()
            approve = Approve(gmt_create = now, gmt_modified = now, applicant_id = userId, applicant_name = userName, approver_id = relation.approver_id, approver_name = relation.approver_name, amount = 0, status = 1)
            session.add(approve)
            session.flush()
            approveRequest = ApproveRequest(gmt_create = now, gmt_modified = now, approve_id = approve.id, memo = param['memo'], status = 1, amount = param['amount'])
            session.add(approveRequest)
            session.flush()
            session.commit()
            res = {'success': True}
            self.write(res)
        except Exception as e:
            logger.exception(e)
            session.rollback()
            res = {'success': False}
            res['errorMsg'] = str(e)
            self.write(res)