#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author  lisongjian@youmi.net
#

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.mission.views',
    # 应用互推
    url(r'^list/$', 'list'),
    url(r'^list/edit/$', 'list_edit'),
    url(r'^list/online/$', 'online'),
    url(r'^list/offline/$', 'offline'),
    url(r'^new/$', 'new'),
)
