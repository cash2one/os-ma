#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author: lisongjian@youmi.net
#

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from apps.mission.models import Mission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connections
#from django.http import HttpResponse
#import json
#import datetime
#from django.template import RequestContext

@login_required
def index(request):
    """ 应用列表 """
    limit = 24
    orderbyud = orderby = request.GET.get('orderby', 'id')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))
    if not updw:
        orderbyud = '-' + orderby
    datas = Mission.objects.order_by(orderbyud)
    if not datas.exists():
        datas = []

    paginator = Paginator(datas, limit)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)
    return render_to_response('count_point/index.html', {
        'title': '计算积分',
        'page_tag': 'count_point',
        'username': request.user.username,
        'datas': datas,
        'orderby':  orderby,
        'updw':     updw,
    })

@login_required
def search(request):
    """ 搜索订单 """
    total, user, avg, cost, roi = get_params(request)
    return render_to_response('count_point/search.html', {
        'title': '搜索结果',
        'page_tag': 'count_point',
        'username': request.user.username,
        'total': total,
        'user': user,
        'avg': avg,
        'cost': cost,
        'roi': roi,
    })

def get_params(request):
    """ 获取参数 """
    total = 0
    count = 0
    query = ''
    query1 = ''
    query2 = ''
    params_user_key = ['apptype', 'platform','en', 'create_at_gte', \
        'create_at_lte', 'time_gte', 'time_lte', 'ad_source']
    for key in params_user_key:
        param = request.GET.get(key)
        if param:
            if param.find('T')!=-1:
                param=timeFormat(param)
            if key!='time_gte' and key!='time_lte' and key!='create_at_gte' and key!='create_at_lte' and key!='ad_source':
                query += " and a.%s='%s'" % (key, param)
                query2 += " and a.%s='%s'" % (key, param)
                if count==0:
                    query1 += " %s='%s'" % (key, param)
                    count +=1
                else:
                    query1 += " and %s='%s'" % (key, param)
            elif key=='create_at_gte':
                query += " and a.`create_at`>='%s'" % (param)
                query1 += " `create_at`>='%s'" % (param)
                query2 += " and a.`create_at`>='%s'" % (param)
            elif key=='create_at_lte':
                query += " and a.create_at<='%s'" % (param)
                query1 += " and create_at<='%s'" % (param)
                query2 += " and a.create_at<='%s'" % (param)
            elif key=='time_gte':
                query += " and b.time>='%s'" % (param)
                query2 += " and b.create_time>='%s'" % (param)
            elif key=='time_lte':
                query += " and b.time<='%s'" % (param)
                query2 += " and b.create_time<='%s'" % (param)
            elif key=='ad_source':
                query += " and b.%s='%s'" % (key, param)
    # 使用原生数据库
    # 统计用户积分
    sql = 'SELECT sum(b.points) FROM `user` AS a, `callback_order` AS b WHERE a.uid=b.user %s' % (query)
    cursor = connections['tipshunter'].cursor()
    cursor.execute(sql)
    raw = cursor.fetchall()
    s=str(list(raw).pop())
    total=s.replace("(Decimal('",'').replace("'),)",'')
    if total.find('None')!=-1:
        total = 0
    # 统计用户数
    sql1 = 'SELECT count(uid) FROM `user` WHERE %s' % (query1)
    cursor.execute(sql1)
    raw1 = cursor.fetchall()
    s1=str(list(raw1).pop())
    user=s1.replace("(",'').replace("L,)",'')
    avg = 0
    if user!=0 and total!=0:
        avg =  "%.2f" % (float(total)/float(user))
    # 兑换订单成本
    sql2 = 'SELECT sum(total_price) FROM `user` AS a, `exchange_orders` AS b WHERE a.uid=b.uid %s and b.status=1' % (query2)
    cursor.execute(sql2)
    raw2 = cursor.fetchall()
    s2=str(list(raw2).pop())
    if s2.find('None')!=-1:
        cost=0
    cost=s2.replace("(Decimal('",'').replace("'),)",'')
    if cost.find('None')!=-1:
        cost=0
    roi=0
    if total!=0 and cost!=0:
        roi =  "%.2f" % ((float(float(total)/100))/float(cost))
    return total, user, avg, cost, roi

def timeFormat(timestr):
    timestr=timestr.replace('T', ' ')+':00'
    return timestr


