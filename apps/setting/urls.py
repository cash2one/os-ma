#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author  lijinsheng@youmi.net, chenjiehua@youmi.net
#

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.setting.views',
    # 广告配置相关
    url(r'^adconfig/$', 'adconfig'),
    url(r'^adconfig/add/$', 'ad_add'),
    url(r'^adconfig/edit/$', 'ad_edit'),
    url(r'^adconfig/del/$', 'ad_del'),

    # 推送通知
    url(r'^push/$', 'push'),

    # 参数配置相关
    url(r'^options/$', 'options'),
    url(r'^options/edit/$', 'opt_edit'),

    # 每日奖励相关
    url(r'^daily/$', 'daily'),
    url(r'^daily/edit/$', 'day_edit'),

    # 帮抢高价
    url(r'^recommend/$', 'recommend'),
    url(r'^recommend/add/$', 're_add'),
    url(r'^recommend/edit/$', 're_edit'),
    url(r'^recommend/del/$', 're_del'),

    # 用户反馈
    url(r'^feedback/$', 'feedback'),
    url(r'^feedback/deal/$', 'deal'),
)
