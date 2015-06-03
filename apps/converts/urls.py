#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author  lijinsheng@youmi.net, chenjiehua@youmi.net
#

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.converts.views',

    # 商品类型 && 添加商品类型
    url(r'^types/$', 'types'),
    # 添加类型
    #url(r'^types/add/$', 'typeAdd'),
    # 编辑类型
    url(r'^types/edit/$', 'typeEdit'),
    # 删除类型
    url(r'^types/delete/$', 'typeDelete'),

    # 添加商品
    url(r'^items/add/$', 'itemAdd'),
    # 编辑商品
    url(r'^items/edit/$', 'itemEdit'),
    # 删除商品
    url(r'^items/delete/$', 'itemDelete'),
    # 兑换商品
    url(r'^items/$', 'items'),
    # 兑换码录入
    url(r'^codes/$', 'codes'),
    # 兑换码信息
    url(r'^codeinfo/$', 'codeinfo'),
    # 允许兑换订单
    url(r'^accept_convert/$', 'acceptConvert'),
    # 添加订单备注
    url(r'^add_notes/$', 'add_notes'),
    # 添加订单兑换码
    url(r'^add_num/$', 'add_num'),
    # 添加订单密码
    url(r'^add_pwd/$', 'add_pwd'),

    # 兑换订单
    url(r'^$', 'index'),
    # 搜索订单
    url(r'^search/$', 'search'),
    # 搜索兑换码
    url(r'^codesearch/$', 'codesearch'),
    # 编辑兑换码
    url(r'^codeinfo/edit/$', 'codeEdit'),
    # 编辑兑换码状态
    url(r'^codeinfo/status/$', 'codeStatus'),
    # 删除兑换码
    url(r'^codeinfo/delete/$', 'codeinfoDelete'),
    # 删除兑换码明细
    url(r'^codedetail/delete/$', 'codedetailDelete'),
    # 兑换码已使用/未使用
    url(r'^codedetail/used/$', 'codedetailUsed'),
    url(r'^codedetail/unused/$', 'codedetailUnused'),
    # 兑换码发放
    url(r'^codedetail/edit/$', 'codedetail_edit'),
    # 兑换卡明细
    url(r'^codedetail/$', 'codedetail'),
    url(r'^codedetail/card/$', 'codedetail'),
    url(r'^codedetail/card/(?P<gid>\d+)/$', 'codedetail'),


)
