#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author  lijinsheng@youmi.net, chenjiehua@youmi.net,lisongjian@youmi.net
#

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.users.views',
    url(r'^$', 'index'),
    url(r'^(?P<gid>\d+)/$', 'index'),
    url(r'^search/$', 'search'),
    url(r'^exchange/(?P<uid>\d+)/$', 'user_exchange'),
    url(r'^detail/(?P<uid>\d+)/$', 'user_detail'),
    url(r'^detail/(?P<uid>\d+)/page/(?P<page>\d+)/$', 'user_detail'),
    url(r'^detail/edit/$', 'user_edit'),
    url(r'^detail/blank/$', 'usersdetailBlank'),
    url(r'^detail/black/$', 'usersdetailBlack'),
    # 怀疑
    url(r'^wonder/$', 'wonder'),
    url(r'^nowonder/$', 'nowonder'),
)
