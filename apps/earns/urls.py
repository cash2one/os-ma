#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author  lijinsheng@youmi.net, chenjiehua@youmi.net
#

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.earns.views',
    url(r'^$', 'index'),
    url(r'^ad/$', 'index'),
    url(r'^ad/(?P<ad>\d+)/$', 'index'),
)
