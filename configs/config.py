#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from ConfigParser import ConfigParser
from cStringIO import StringIO

from utils.utils import FancyDict


DEFAULT_FILE_NAME = 'config.ini'


def _load_column_configs(column='config', config_ini_name=DEFAULT_FILE_NAME):
    _cp = ConfigParser()
    current_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_path, config_ini_name)
    with open(file_path, 'rb') as fp:
        content = fp.read()
    content = content.replace('\xef\xbb\xbf', '')
    fp = StringIO(content)
    _cp.readfp(fp)
    return _cp.items(column)


def load_column_configs(column, config_ini_name):
    configs = _load_column_configs(column, config_ini_name)
    if configs:
        configs = dict(configs)
    else:
        configs = dict()
    configs = FancyDict(configs)
    return configs


class IniConfig(object):

    def __getattribute__(self, *args, **kwargs):
        column = args[0]
        configs = load_column_configs(column, DEFAULT_FILE_NAME)
        return configs


ini_config = IniConfig()
