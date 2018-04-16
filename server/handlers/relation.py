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
        relation = session.query(ApproveRelation).filter(and_(ApproveRelation.applicant_id == userId, ApproveRelation.approver_id.isnot(None))).first()
        res = None
        try:
            if relation:
                res = {'success': True}
                self.write(res)
                return
            now = time.localtime()
            relation = ApproveRelation(gmt_create = now, gmt_modified = now, applicant_id = userId, applicant_name = userName)
            session.add(relation)
            session.commit()
            res = {'success': True}
        except Exception as e:
            session.rollback()
            logger.exception(e)
            res = {'success': False, 'errorMsg': str(e)}
        self.write(res)

class QueryRelationHandler(BaseHandler):
    @authenticated
    def get(self):
        userId = self.get_current_user_id()
        relation = session.query(ApproveRelation).filter(and_(ApproveRelation.applicant_id == userId, ApproveRelation.approver_id.isnot(None))).first()
        res = None
        if relation:
            res = {'success': True}
        else:
            res = {'success': False}
        self.write(res)

class AcceptRelationHandler(BaseHandler):
    @authenticated
    def post(self):
        param = self.request.body.decode('utf-8')
        param = json.loads(param)
        logger.info(param)
        userId = self.get_current_user_id()
        userName = self.get_current_user_name()
        relation = session.query(ApproveRelation).filter(and_(ApproveRelation.applicant_id == param['applicantId'], ApproveRelation.approver_id.isnot(None))).first()
        res = None
        try:
            if relation:
                res = {'success': True}
                self.write(res)
                return
            now = time.localtime()
            relation.approver_id = userId
            relation.approver_name = userName
            relation.gmt_modified = now
            session.flush()
            session.commit()
            res = {'success': True}
        except Exception as e:
            session.rollback()
            logger.exception(e)
            res = {'success': False, 'errorMsg': str(e)}
        self.write(res)
        
