#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from tornado.web import RequestHandler


RE_USER_AGENT = re.compile(r'(iPhone|iPod|Android|ios|iPad)')
RE_IOS_USER_AGENT = re.compile(r'(iPhone|iPod|ios|iPad)')


class BasePageHandler(RequestHandler):

    def initialize(self):
        super(BasePageHandler, self).initialize()
        self.is_wap = 0
        self.is_ios = False

        self.http_referer = self.request.headers.get('Referer', '')
        self.user_agent = self.request.headers.get('user-agent', '')
        self.remote_ip = self.request.remote_ip
        self.uri = self.request.uri

        self._check_is_wap()

    def _check_is_wap(self):
        if self.user_agent != '' and RE_USER_AGENT.search(self.user_agent):
            self.is_wap = 1
            if RE_IOS_USER_AGENT.search(self.user_agent):
                self.is_ios = True
