#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import logging
import time
import re
import signal

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.log

from configs.config import ini_config
from apps.api import reg_api_resources


tornado.options.define("port", default=8083, help="run on the given port", type=int)
APPLICATION = None
HTTP_SERVER = None


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
            'title': '区块链首支中文单曲来啦',
            'keywords': '区块链首支中文单曲来啦',
            'description': '区块链首支中文单曲来啦',
        }
        if self.is_wap:
            self.page_get = 'first/wap_home.html'
        else:
            self.page_get = 'first/pc_home.html'
        self.render(self.page_get, page_param=page_param)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
           (r'/', IndexHandler),
        ]
        config_instance = ini_config
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "views"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True if int(ini_config.server.debug) else False,
            xsrf_cookies=True if int(ini_config.server.xsrf_cookies) else False,
            autoreload=True if int(ini_config.server.autoreload) else False,
            cookie_secret=ini_config.server.cookie_secret,
        )

        tornado.web.Application.__init__(self, handlers, **settings)

        self.shutdown_listener = []
        # add init handlers here
        reg_api_resources(self)

    def destroy(self):
        for listener in self.shutdown_listener:
            listener.destroy()

    def register_shutdown(self, listener):
        self.shutdown_listener.append(listener)


def sig_handler(sig, frame):
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    global APPLICATION
    global HTTP_SERVER
    # 不接收新的 HTTP 请求
    HTTP_SERVER.stop()

    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + 5

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            # 处理完现有的 callback 和 timeout 后，可以跳出 io_loop.start() 里的循环
            io_loop.stop()

    stop_loop()
    APPLICATION.destroy()


def app_log_add_handler():
    if tornado.options.options.log_file_prefix:
        file_path = tornado.options.options.log_file_prefix
        file_path = '{}_error.log'.format(file_path)
        log_handler = logging.handlers.TimedRotatingFileHandler(
            filename=file_path,
            when='midnight',
            interval=1,
            backupCount=10
        )
        log_handler.setFormatter(tornado.log.LogFormatter(color=False))
        tornado.log.app_log.setLevel('INFO')
        tornado.log.app_log.addHandler(log_handler)


def main():
    global APPLICATION, HTTP_SERVER
    tornado.options.parse_command_line()
    APPLICATION = Application()
    HTTP_SERVER = tornado.httpserver.HTTPServer(APPLICATION, xheaders=True)
    HTTP_SERVER.listen(tornado.options.options.port)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    # 给app_log添加handler
    app_log_add_handler()

    loop = tornado.ioloop.IOLoop.instance()
    loop.start()


if __name__ == '__main__':
    main()
