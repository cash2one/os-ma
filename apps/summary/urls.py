#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author  lijinsheng@youmi.net
#

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.summary.views',
    url('^$', 'index'),
    url(r'^earns/$', 'earns'),
    url(r'^income/$', 'income'),
    url(r'^income/edit/$', 'income_edit'),
    url(r'^income/count/$', 'income_count'),
)
