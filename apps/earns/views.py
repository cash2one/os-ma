#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author chenjiehua@youmi.net
#

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from datetime import datetime, timedelta
from apps.earns.models import Callback, AdConfig


@login_required
def index(request, ad=0):
    """ 订单管理 """
    ad = int(ad)
    cur_ad = {}
    cur_ad['id'] = ad

    # 广告配置信息
    adconfig = AdConfig.objects.exclude(ad_id=100).exclude(ad_id=105). \
        exclude(ad_id=111).exclude(ad_id=112).exclude(ad_id=116). \
        exclude(ad_id=102).order_by('ad_id')
    for a in adconfig:
        if a.ad_id == ad:
            cur_ad['name'] = a.description
    if not ad:
        cur_ad['name'] = '全部'

    date = request.GET.get('date')
    enddate = request.GET.get('enddate')
    page = request.GET.get('page')

    if not page:
        page = 1

    if not date:
        date_start = datetime.strftime(datetime.now(), "%Y-%m-01")
        date_end = datetime.strftime(datetime.now()+timedelta(days=1), "%Y-%m-%d")
    else:
        date_start = date
        #date_end = datetime.strftime(datetime.strptime(date, "%Y-%m-%d")+timedelta(days=1), "%Y-%m-%d")
        date_end = enddate

    if ad:
        orders = Callback.objects.filter(
            ad_source=ad, time__gte=date_start, time__lt=date_end).order_by('-time')
    else:
        orders = Callback.objects.filter(
            time__gte=date_start, time__lt=date_end).order_by('-time')

    # 总下载数，总积分
    summary = dict(
        count=orders.count(),
        points=orders.aggregate(Sum('points'))['points__sum'],
    )
    # 分页
    limit = 25
    paginator = Paginator(orders, limit)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render_to_response('earns/index.html', {
        'title':    '赚取效果',
        'page_tag': 'earns',
        'username': request.user.username,
        'datas': orders,
        'ad': adconfig,
        'cur_ad': cur_ad,
        'query_date': date_start,
        'query_enddate': date_end,
        'summary': summary,
    })
