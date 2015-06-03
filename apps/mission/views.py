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
from django.http import HttpResponse
import json
import datetime
from django.template import RequestContext

@login_required
def list(request):
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
    return render_to_response('mission/list.html', {
        'title': '应用列表',
        'page_tag': 'mission',
        'username': request.user.username,
        'datas': datas,
        'orderby':  orderby,
        'updw':     updw,
    })

@login_required
def online(request):
    """
        应用开启
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认删除
    if gid:
        mission = Mission.objects.get(id=gid)
    mission.status=1
    mission.save()
    res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def offline(request):
    """
        应用关闭
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认删除
    if gid:
        mission = Mission.objects.get(id=gid)
    mission.status=0
    mission.save()
    res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def new(request):
    """ 发布任务 """
    mission = Mission.objects.all()
    posts = {}
    errors = []
    succ = False
    if request.method == 'POST':
        posts = {
                'icon' : request.POST.get('icon', ''),
                'desc_url' : request.POST.get('desc_url', ''),
                'title' : request.POST.get('title', ''),
                'description' : request.POST.get('description', ''),
                'point' : request.POST.get('point', ''),
                'limit' : request.POST.get('limit', ''),
                'time_limit':    int(request.POST.get('time_limit', 0)),
                'number_limit':    int(request.POST.get('number_limit', 0)),
                'edate' : request.POST.get('edate', ''),
                'stime' : request.POST.get('stime', ''),
                'total' : request.POST.get('total', ''),
        }
        if not posts['icon']:
            errors.append("请输入图片地址")
        if not posts['desc_url']:
            errors.append("请输入描述图片地址")
        if not posts['title']:
            errors.append("请输入标题")
        if not posts['description']:
            errors.append("请输入描述")
        if not posts['point']:
            errors.append("请输入积分")
        if not posts['limit']:
            errors.append("请输入每日限量")
        if not posts['time_limit']:
            errors.append("请输入是否限时")
        if not posts['number_limit']:
            errors.append("请输入是否限量")
        if not errors:
            Mission.objects.create(icon=posts['icon'], desc_url=posts['desc_url'], title=posts['title'], number_limit=posts['number_limit'], \
                description=posts['description'], point=posts['point'], time_limit = posts['time_limit'], \
                rest=posts['total'], total=posts['total'], status=1, etime=posts['edate'], stime= posts['stime'], limit=posts['limit'])
            succ = True

    return render_to_response('mission/push.html', {
        'title': '发布自有任务',
        'page_tag': 'mission',
        'username': request.user.username,
        'datas': mission,
        'errors': errors,
        'succ' : succ,
    }, context_instance=RequestContext(request))

@login_required
def list_edit(request):
    """ 任务修改 """
    errors = []
    succ = False
    if request.method == 'GET':
        id = request.GET.get('id', 0)
        if id:
            datas = Mission.objects.get(id=id)
            print `datas.stime.date()`+'1111111111111111111111'
        else:
            return None
    elif request.method == 'POST':
        datas = {
            'id':           int(request.POST.get('id', 0)),
            'icon':       request.POST.get('icon', ''),
            'desc_url':       request.POST.get('desc_url', ''),
            'title':       request.POST.get('title', ''),
            'description':       request.POST.get('description', ''),
            'limit':       request.POST.get('limit', ''),
            'point':       request.POST.get('point', 0),
            'total':       request.POST.get('total', 0),
            'time_limit':       request.POST.get('time_limit', 0),
            'number_limit':       request.POST.get('number_limit', 0),
            'rest':       request.POST.get('rest', 0),
            # 'stime':       request.POST.get('stime', ''),
            # 'etime':       request.POST.get('etime', ''),
        }
        if datas['id']:
            Mission.objects.filter(id=datas['id']).update(icon=datas['icon'], desc_url=datas['desc_url'], \
                title=datas['title'], description=datas['description'], limit=datas['limit'], \
                point=datas['point'], total=datas['total'], time_limit=datas['time_limit'], \
                number_limit=datas['number_limit'], rest=datas['rest'])
            #,stime=datas['stime'], etime=datas['etime'])
        succ = True
    else:
        return None
    return render_to_response('mission/mission_edit.html', {
        'title': '编辑任务',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas': datas,
        'succ': succ,
        'errors': errors,
    })
