#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import traceback
import uuid

from data_access import MysqlInstance
from utils.timeutil import get_now_str


def get_my_code_by_mobile(mobile):
    db_obj = MysqlInstance.instance().db
    sql = 'select code from user where phone="{}";'.format(mobile)
    entries = MysqlInstance.query(db_obj, sql)
    if entries:
        my_code = entries[0]['code']
    else:
        my_code = ''
    return my_code


def create_invitation(mobile, address, invitation_code):
    try:
        db_obj = MysqlInstance.instance().db
        code = uuid.uuid1().hex
        param_dict = dict(
            phone=mobile, code=code, invitation_code=invitation_code, address=address, create_time=get_now_str()
        )
        sql = MysqlInstance.gen_insert_sql('user', param_dict)
        entries = MysqlInstance.execute(db_obj, sql)
        logging.info('entries:{}'.format(entries))
    except:
        code = ''
        logging.error(traceback.format_exc())

    return code
