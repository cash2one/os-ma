#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author  lisongjian@youmi.net
#

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.count_point.views',
    url(r'^$', 'index'),
    # 搜索
    url(r'^search/$', 'search'),
)
