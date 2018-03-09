#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import torndb

from utils.timeutil import get_now

from configs.config import ini_config


class MysqlInstance(object):
    @staticmethod
    def instance():
        if not hasattr(MysqlInstance, "_instance"):
            # New instance
            MysqlInstance._instance = MysqlInstance()
        return MysqlInstance._instance

    def __init__(self):
        self.db = self.gen_db_conn()

    def gen_db_conn(self):
        db_conn = torndb.Connection(
            host=ini_config.mysql.host,
            database=ini_config.mysql.db,
            user=ini_config.mysql.user,
            password=ini_config.mysql.password
        )
        return db_conn

    @staticmethod
    def _parse_sql(param_dict):
        key_list = ''
        value_list = ''
        for key in param_dict:
            value = param_dict[key]
            if value != None:
                key_list += '%s, ' % key
                if isinstance(value, str):
                    value = value.replace("'", '"')
                    value_list += "'%s', " % value
                elif isinstance(value, int) or isinstance(value, long):
                    value_list += "%d, " % value
                else:
                    value_list += "'%s', " % value

        if key_list != '':
            key_list = key_list[:-2]
        if value_list != '':
            value_list = value_list[:-2]
        return key_list, '(' + value_list + ')'

    @staticmethod
    def gen_insert_sql(table, param_dict):
        key_list, value_list = MysqlInstance._parse_sql(param_dict)
        return 'INSERT INTO %s (%s) VALUES %s' % (table, key_list, value_list)

    @staticmethod
    def gen_insert_many(table, param_list):
        key_list = ''
        values = []

        for param_dict in param_list:
            key_list, value_list = MysqlInstance._parse_sql(param_dict)
            values.append(value_list)

        return 'INSERT INTO %s (%s) VALUES %s' % (table, key_list, ','.join(values))

    @staticmethod
    def gen_update_sql(table, param_dict):

        sql_exp = "UPDATE %s SET " % table
        for key in param_dict:
            value = param_dict[key]
            if isinstance(value, str):
                value = value.replace("'", '"')
                sql_exp += "%s = '%s'," % (key, value)
            elif isinstance(value, int) or isinstance(value, long):
                sql_exp += "%s = %d," % (key, value)
            else:
                value = value.replace("'", '"')
                sql_exp += "%s = '%s'," % (key, value)
        sql_exp = sql_exp[:-1] + " "
        return sql_exp

    @staticmethod
    def query(db, sql_exp):
        result = None
        begin_time = get_now()
        try:
            logging.info('[mysql_db] query sql:"{}"'.format(sql_exp))
            result = db.query(sql_exp)
        finally:
            cost_time = (get_now() - begin_time).total_seconds()
            logging.info('[mysql_db] query sql:"%s". cost %ss' % (sql_exp, cost_time))
        return result

    @staticmethod
    def execute(db, sql_exp):
        logging.info('[mysql_db] exec sql:"{}"'.format(sql_exp))
        return db.execute(sql_exp)

    @staticmethod
    def execute_rowcount(db, sql_exp):
        result = None
        begin_time = get_now()
        try:
            result = db.execute_rowcount(sql_exp)
        finally:
            cost_time = (get_now() - begin_time).total_seconds()
            logging.info('[mysql_db] exec sql:"%s". cost %ss' % (sql_exp, cost_time))
        return result
