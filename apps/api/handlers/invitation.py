#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import logging
import traceback

from tornado.gen import coroutine

from apps.api.api_base import ApiBaseHandler
from data_access.user_table import get_my_code_by_mobile, create_invitation


class InvitationSearchHandler(ApiBaseHandler):
    def initialize(self):
        super(InvitationSearchHandler, self).initialize()

    @coroutine
    def post(self):
        mobile = self.get_body_argument('mobile', '')
        error_msg = '' if 1 <= len(mobile) <= 20 else u'手机号不合法'
        if not error_msg:
            my_code = get_my_code_by_mobile(mobile)
            if my_code:
                status = 1
            else:
                status = 0
            link = self.get_share_link(my_code)
            data = {
                "mobile": mobile,
                "link": link,
            }
        else:
            status = 2
            data = {}
        self.build_json_response(status=status, msg=error_msg, data=data)

    def get_share_link(self, code):
        return 'http://www.ipmarket.top?id={}'.format(code)


class InvitationCreateHandler(ApiBaseHandler):
    def initialize(self):
        super(InvitationCreateHandler, self).initialize()

    @coroutine
    def post(self):
        mobile = self.get_body_argument('mobile', '')
        address = self.get_body_argument('address', '')
        path = self.get_body_argument('path', '')

        invitation_code = path.split('id=')[-1].split('&')[0]
        if not invitation_code:
            invitation_code = ''
        if '.' in invitation_code or '/' in invitation_code:
            invitation_code = ''
        logging.info(
            'mobile:{}, address:{}, path:{}, invitation_code:{}'.format(mobile, address, path, invitation_code)
        )
        data = {}
        error_msg = '' if 1 <= len(mobile) <= 20 else u'手机号不合法'
        if not error_msg:
            error_msg = '' if 1 <= len(address) <= 100 else u'地址不合法'
        if not error_msg:
            my_code = get_my_code_by_mobile(mobile)
            if my_code:
                error_msg = u'数据不合法'
        if not error_msg:
            my_code = create_invitation(mobile, address, invitation_code)
            if not my_code:
                status = 2
                error_msg = u'网络繁忙, 请稍后重试'
            else:
                status = 0
                link = self.get_share_link(my_code)
                data = {
                    "mobile": mobile,
                    "link": link,
                }
        else:
            status = 1
        self.build_json_response(status=status, msg=error_msg, data=data)

    def get_share_link(self, code):
        return 'http://www.ipmarket.top?id={}'.format(code)
