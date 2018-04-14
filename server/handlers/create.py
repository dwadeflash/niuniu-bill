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

class CreateHandler(BaseHandler):
    # @authenticated
    def post(self):
        try:
            param = self.request.body.decode('utf-8')
            param = json.loads(param)
            now = time.localtime()
            userId = self.get_current_user_id()
            userName = self.get_current_user_name()
            relation = session.query(ApproveRelation).filter(ApproveRelation.applicant_id == userId).first()
            approve = Approve(gmt_create = now, gmt_modified = now, applicant_id = userId, applicant_name = userName, approver_id = param['approverId'], approver_name = relation.approver_name, amount = 0, status = 1)
            session.add(approve)
            session.flush()
            approveRequest = ApproveRequest(gmt_create = now, gmt_modified = now, approve_id = approve.id, memo = param['memo'], status = 1, amount = param['amount'])
            session.add(approveRequest)
            session.flush()
            session.commit()
            res = {'success': "true"}
            self.write(res)
        except Exception as e:
            res = {'success': "false"}
            res['errorMsg'] = str(e)
            self.write(res)