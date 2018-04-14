# coding:utf-8

from datetime import datetime

class ApproveVO:
    id = 0
    gmt_create = None
    gmt_modified = None
    applicantId = 0
    applicantName = None
    approverId = 0
    approverName = None
    status = 0
    statusStr = None
    requestAmount = 0
    approvedAmount = 0
    requestMemo = ""
    approveMemo = ""

    def __init__(self, approve, approveRequest, approveRecord):
        self.id = approve.id
        self.gmt_create = approve.gmt_create
        self.gmt_modified = approve.gmt_modified
        self.applicantId = approve.applicant_id
        self.applicantName = approve.applicant_name
        self.approverId = approve.approver_id
        self.approverName = approve.approver_name
        self.status = approve.status
        self.approveAmount = approve.amount
        if self.status == 1:
            self.statusStr = "待审批"
        elif self.status == 2:
            self.statusStr = "同意"
        elif self.status == 3:
            self.statusStr = "不同意"
        elif self.status == 4:
            self.statusStr = "部分同意"
        if approveRequest:
            self.requestAmount = approveRequest.amount
            self.requestMemo = approveRequest.memo
        if approveRecord:
            self.approveMemo = approveRecord.memo
    
    def default(self):
        return self.__dict__
