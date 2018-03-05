#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import logging
import hashlib
import re

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import traceback
tornado.options.define("port", default=8083, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):

    def initialize(self):
        super(IndexHandler, self).initialize()
        self.is_wap = 0
        self.is_ios = False
        self.re_user_agent = re.compile(r'(iPhone|iPod|Android|ios|iPad)')
        self.re_ios_user_agent = re.compile(r'(iPhone|iPod|ios|iPad)')
        self._check_is_wap()
        self.http_referer = self.request.headers.get('Referer', '')

    def _check_is_wap(self):
        user_agent = self.request.headers.get('user-agent', '')
        if user_agent != '' and self.re_user_agent.search(user_agent):
            self.is_wap = 1
            if self.re_ios_user_agent.search(user_agent):
                self.is_ios = True

    def get(self):
        page_param = {
            'title': 'IP MARKET',
            'keywords': 'IP MARKET',
            'description': 'IP MARKET',
            }
        if self.is_wap:
            self.page_get = 'first/wap_home.html'
        else:
            self.page_get = 'first/pc_home.html'
        self.render(self.page_get, page_param=page_param)

def main():
    print os.path.dirname(__file__)
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[

          (r'/', IndexHandler),
          ],
        template_path=os.path.join(os.path.dirname(__file__), "views"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="61oETzKXQAGaYdghdhgfhfhfg",
        debug=True,
        autoreload=True
    )
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()