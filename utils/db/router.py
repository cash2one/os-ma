#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 数据库路由
#

"""
    可以让 db 单独设置 connection
    @see   http://stackoverflow.com/questions/3637419/multiple-database-config-in-django-1-2
"""
from config.settings import ADMIN_DATABASE

class DBRouter(object):
    """
        可以按照 model 里面的 connection_name 来设置要读的数据库
    """
    def db_for_read(self, model, **hints):
        # 对于django内置的表，全部使用另外一个表
        prefix = model.__module__.split('.')[0]
        if prefix == "django" or prefix == "utils":
            return ADMIN_DATABASE
        elif hasattr(model, 'connection_name'):
            return model.connection_name
        return None

    def db_for_write(self, model, **hints):
        prefix = model.__module__.split('.')[0]
        if prefix == "django" or prefix == "utils":
            return ADMIN_DATABASE
        elif hasattr(model, 'connection_name'):
            return model.connection_name
        return None

    def allow_syncdb(self, db, model):
        prefix = model.__module__.split('.')[0]
        if prefix == "django" or prefix == "utils":
            if db == ADMIN_DATABASE:
                return True
            else:
                return False
        elif hasattr(model, 'connection_name'):
            if model.connection_name == db:
                return True
            else:
                return False
        else:
            if db == "default":
                return True
            else:
                return False
        return None
