#!/usr/bin/env python3
# coding:utf-8

from handlers.base import BaseHandler
from models.User import User
from models.ApproveRelation import ApproveRelation
from dao.base import session

import logging
logger = logging.getLogger('boilerplate.' + __name__)

import requests
import json
import jsonpickle
from tornado.web import authenticated
import time
from sqlalchemy import *

class MakeRelationHandler(BaseHandler):
    @authenticated
    def post(self):
        param = self.request.body.decode('utf-8')
        param = json.loads(param)
        logger.info(param)
        userId = self.get_current_user_id()
        userName = self.get_current_user_name()
        relation = session.query(ApproveRelation).filter(ApproveRelation.applicant_id == userId).first()
        try:
            if relation:
                res = {'success': True}
                self.write(res)
                return
            ticket = param['ticket']
            relation = ApproveRelation(gmt_create = now, gmt_modified = now, applicant_id = userId, applicant_name = userName, approver_id = relation.approver_id, approver_name = relation.approver_name)

