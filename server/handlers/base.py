# coding:utf-8

import json
import tornado.web
from tornado.options import options
import base64
import M2Crypto
import hashlib, time

import logging
logger = logging.getLogger('boilerplate.' + __name__)

from dao.base import r


class BaseHandler(tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                    "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg

    def get_current_user(self):
        sessionId = self.getSessionId()
        if sessionId:
            user = r.get(sessionId)
            if user:
                return json.loads(r.get(sessionId))
            else:
                return None
        else:
            return None

    def get_current_user_id(self):
        user = self.get_current_user()
        if not user:
            return None
        else:
            return user['id']

    def get_current_user_name(self):
        user = self.get_current_user()
        if not user:
            return None
        else:
            return user['nickName']

    def generateSessionId(self):
        '''
        m = hashlib.md5()
        m.update('this is a test of the emergency broadcasting system')
        m.update(str(time.time()))
        m.update(str('aaaa'))
        return base64.encodebytes(m.hexdigest)[:-3]
        '''
        return base64.b64encode(M2Crypto.m2.rand_bytes(16)).decode()

    def set_secure_session(self, sessionId, userInfo, expireSeconds = options.redisexpire):
        r.set(sessionId, userInfo, expireSeconds)

    def getSessionId(self):
        return self.request.headers.get('sessionId')