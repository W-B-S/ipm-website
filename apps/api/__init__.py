#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urls import HANDLERS


def reg_api_resources(application):
    application.add_handlers(r".*", HANDLERS)
