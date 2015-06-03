#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author: lisongjian@youmi.net
#

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from apps.go_mission.models import Go_mission
from apps.mission.models import Mission
from apps.users.models import Users, GlobalOrders, CallbackOrders
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
import datetime
import json

@login_required
def list(request):
    """ 应用列表 """
    limit = 24
    orderbyud = orderby = request.GET.get('orderby', 'id')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))
    if not updw:
        orderbyud = '-' + orderby
    datas = Go_mission.objects.order_by(orderbyud)
    if not datas.exists():
        datas = []

    paginator = Paginator(datas, limit)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)
    return render_to_response('go_mission/list.html', {
        'title': '用户任务列表',
        'page_tag': 'go_mission',
        'username': request.user.username,
        'datas': datas,
        'orderby':  orderby,
        'updw':     updw,
    })

@login_required
def online(request):
    """
        任务完成
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认删除
    if gid:
        go_mission = Go_mission.objects.get(id=gid)
    go_mission.status=2
    go_mission.save()
    res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def offline(request):
    """
        任务失败
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认删除
    if gid:
        go_mission = Go_mission.objects.get(id=gid)
    go_mission.status=3
    go_mission.save()
    res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def new(request):
    """ 用户完成 """
    go_mission = Go_mission.objects.all()
    posts = {}
    errors = []
    succ = False
    today = datetime.datetime.now().date()
    yesterday= today-datetime.timedelta(days=1)
    if request.method == 'POST':
        posts = {
                'iv_code' : request.POST.get('iv_code', ''),
                'mission_id' : request.POST.get('mission_id', 0),
        }
        if not posts['iv_code']:
            errors.append("请输入用户邀请码")
        if not posts['mission_id']:
            errors.append("请输入任务id")
        if not errors:
            user = get_object_or_404(Users, invited_code=posts['iv_code'])
            Go_mission.objects.create(iv_code=posts['iv_code'], mission_id=posts['mission_id'], uid=int(user.uid), \
                status=2, stime=yesterday)
            succ = True

    return render_to_response('go_mission/push.html', {
        'title': '用户完成任务',
        'page_tag': 'go_mission',
        'username': request.user.username,
        'datas': go_mission,
        'errors': errors,
        'succ' : succ,
    }, context_instance=RequestContext(request))

@login_required
def edit(request):
    """ 任务修改 """
    errors = []
    succ = False
    if request.method == 'GET':
        gid = request.GET.get('gid', 0)
        if gid:
            datas = Go_mission.objects.get(id=gid)
        else:
            return None
    elif request.method == 'POST':
        datas = {
            'id':           int(request.POST.get('id', 0)),
            'uid':       request.POST.get('uid', 0),
        }
        if datas['id']:
            mission = get_object_or_404(Mission, id=datas['id'])
            add_points = mission.point
            user = get_object_or_404(Users, uid=datas['uid'])
            Users.objects.filter(uid=datas['uid']).update(points=(int(user.points)+int(add_points)))
            GlobalOrders.objects.create(uid=datas['uid'], type='6', note=mission.title, \
                last=int(user.points), points=int(add_points))
            CallbackOrders.objects.create(order=mission.title, ad_source='16', platform=3, ad=mission.title, \
                user=datas['uid'], points=int(add_points))
        succ = True
    else:
        return None
    return render_to_response('go_mission/edit.html', {
        'title': '发放奖励',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas': datas,
        'succ': succ,
        'errors': errors,
    })

