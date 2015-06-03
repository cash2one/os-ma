#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author: lisongjian@youmi.net
#

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from apps.popularize.models import Popularize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import json
from django.template import RequestContext

@login_required
def list(request):
    """ 应用列表 """
    limit = 25
    orderbyud = orderby = request.GET.get('orderby', 'id')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))
    if not updw:
        orderbyud = '-' + orderby
    datas = Popularize.objects.order_by(orderbyud)
    if not datas.exists():
        datas = []

    paginator = Paginator(datas, limit)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)
    return render_to_response('popularize/list.html', {
        'title': '应用列表',
        'page_tag': 'popularize',
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
        popularize = Popularize.objects.get(id=gid)
    popularize.status=1
    popularize.save()
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
        popularize = Popularize.objects.get(id=gid)
    popularize.status=0
    popularize.save()
    res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def push(request):
    """ 发布公告 """
    popularize = Popularize.objects.all()
    import os
    from config.settings import POPULARIZE_DIR, BASE_DIR
    import Image
    posts = {}
    errors = []
    succ = False
    sw = 72
    sh = 72
    if request.method == 'POST':
        file_obj = request.FILES.get('popularizeIcon', None)
        posts = {
                'pushTitle' : request.POST.get('pushTitle', ''),
                'pushContent' : request.POST.get('pushContent', ''),
                'pname' : request.POST.get('pname', ''),
                'url' : request.POST.get('url', ''),
                'Apush':    int(request.POST.get('Apush', 0)),
        }
        if not file_obj:
            errors.append("请输入应用图标")
        else:
            image = Image.open(file_obj)
            (width, height) = image.size
            if width > sw or height > sh:
                errors.append("图标规格不正确，请选择至多72*72的图标上传")
        if not posts['pushTitle']:
            errors.append("请输入应用标题")
        if not posts['pushContent']:
            errors.append("请输入应用推荐语")
        if not posts['pname']:
            errors.append("请应用包名")
        if not posts['url']:
            errors.append("请输入应用下载地址")
        if not errors:
            file_name = file_obj.name
            name = POPULARIZE_DIR
            file_dir = os.path.join(BASE_DIR, name)
            Popularize.objects.create(title=posts['pushTitle'],content=posts['pushContent'], \
                icon=file_name, url=posts['url'], status=posts['Apush'], pname = posts['pname'])
            file_dir = file_dir + file_name
            posts['popularizeIcon'] = 'popularize/' + file_name
            with open(file_dir, 'wb') as dest:
                for chunk in file_obj.chunks():
                    dest.write(chunk)
            succ = True

    return render_to_response('popularize/push.html', {
        'title': '应用推广',
        'page_tag': 'popularize',
        'username': request.user.username,
        'datas': popularize,
        'errors': errors,
        'succ' : succ,
    }, context_instance=RequestContext(request))


