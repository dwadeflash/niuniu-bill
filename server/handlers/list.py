# coding:utf-8

from handlers.base import BaseHandler
from models.Approve import Approve
from models.ApproveRequest import ApproveRequest
from models.ApproveRecord import ApproveRecord
from models.ApproveVO import ApproveVO
from dao.base import session
from util.cjson import CJsonEncoder

import logging
logger = logging.getLogger('boilerplate.' + __name__)

import requests
import json
import jsonpickle
from tornado.web import authenticated
import time
from sqlalchemy import *

class ListHandler(BaseHandler):
    @authenticated
    def get(self):
        userId = self.get_current_user_id()
        try:
            approves = session.query(Approve).filter(or_(Approve.applicant_id==userId, Approve.approver_id==userId)).order_by("gmt_modified desc").all()
            approveRequests = session.query(ApproveRequest).filter(ApproveRequest.approve_id.in_([item.id for item in approves])).order_by("gmt_modified desc").all()
            approveRecords = session.query(ApproveRecord).filter(ApproveRecord.approve_request_id.in_([item.id for item in approveRequests])).order_by("gmt_modified desc").all()
            data = []
            for approve in approves:
                request = [item for item in approveRequests if item.approve_id == approve.id][0]
                records = [item for item in approveRecords if item.approve_request_id == request.id]
                record = None
                if len(records) > 0:
                    record = records[0]
                data.append(ApproveVO(approve, request, record))
            res = {'success': True, 'data': data}
        except Exception as e:
            print(e)
            res = {'success': False}
            res['errorMsg'] = str(e)
        self.write(jsonpickle.encode(res, unpicklable=False))