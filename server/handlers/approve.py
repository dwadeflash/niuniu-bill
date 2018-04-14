from handlers.base import BaseHandler
from models.Approve import Approve
from models.ApproveRequest import ApproveRequest
from models.ApproveRecord import ApproveRecord
from dao.base import session

import logging
logger = logging.getLogger('boilerplate.' + __name__)

import requests
import json
from tornado.web import authenticated
import time

class ApproveHandler(BaseHandler):
    # @authenticated
    def post(self):
        res = {}
        try:
            param = self.request.body.decode('utf-8')
            param = json.loads(param)
            print(param)
            now = time.localtime()
            userId = self.get_current_user_id()
            approve = session.query(Approve).filter(Approve.id == param['approveId'], Approve.approver_id == userId).first()
            if approve == None:
                raise Exception("can't find Approve, id="+str(param['approveId']))
            approveRequest = session.query(ApproveRequest).filter(ApproveRequest.approve_id == approve.id, ApproveRequest.status == 1).first()
            if approveRequest == None:
                raise Exception("can't find ApproveRequest, approve_id=" + str(approve.id) + ", status=1")
            approveRecord = ApproveRecord(gmt_create = now, gmt_modified = now, approve_request_id = approveRequest.id, status = param['status'], memo = param['memo'])
            approve.status = param['status']
            approve.gmt_modified = now
            if approve.status == 2 or approve.status == 3 :
                approve.amount = param['amount']
            approveRequest.status = param['status']
            approveRequest.gmt_modified = now
            session.flush()
            session.add(approveRecord)
            session.commit()
            res['success'] = True
        except Exception as e:
            print(e)
            res['success'] = False
            res['errorMsg'] = str(e)
        self.write(res)