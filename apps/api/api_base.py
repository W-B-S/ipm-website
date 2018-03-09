#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging

from apps.page_base import BasePageHandler


class ApiBaseHandler(BasePageHandler):

    def initialize(self):
        super(ApiBaseHandler, self).initialize()

    def build_json_response(self, status, msg='', data=None):
        result = {
            'status': status,
            'msg': msg,
            'data': data
        }
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        json_result = json.dumps(result)
        self.write(json_result)
        logging.info('json_result:{}'.format(json_result))
        return json_result
