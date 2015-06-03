#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author  lijinsheng@youmi.net
#

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.blacklist.views',


    # 黑名单
    url(r'^iplist/$', 'iplist'),
    url(r'^maillist/$', 'maillist'),
    url(r'^ipadd/$', 'ipadd'),
    url(r'^mailadd/$', 'mailadd'),
    url(r'^imeilist/$', 'imeilist'),
    url(r'^idfalist/$', 'idfalist'),
    url(r'^imeiadd/$', 'imeiadd'),
    url(r'^idfaadd/$', 'idfaadd'),
    url(r'^uidlist/$', 'uidlist'),
    url(r'^uidadd/$', 'uidadd'),

)
