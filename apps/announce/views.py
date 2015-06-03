#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author: lisongjian@youmi.net
#

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from apps.announce.models import Announce
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import json
from django.template import RequestContext
from datetime import date

@login_required
def list(request):
    """ 公告列表 """
    limit = 25
    orderbyud = orderby = request.GET.get('orderby', 'id')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))
    if not updw:
        orderbyud = '-' + orderby
    datas = Announce.objects.order_by(orderbyud)
    if not datas.exists():
        datas = []

    paginator = Paginator(datas, limit)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)
    return render_to_response('announce/list.html', {
        'title': '公告列表',
        'page_tag': 'announce',
        'username': request.user.username,
        'datas': datas,
        'orderby':  orderby,
        'updw':     updw,
    })

@login_required
def online(request):
    """
        公告上线
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认删除
    if gid:
        announce = Announce.objects.get(id=gid)
    announce.online=1
    announce.save()
    res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def offline(request):
    """
        公告下线
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认删除
    if gid:
        announce = Announce.objects.get(id=gid)
    announce.online=0
    announce.save()
    res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def push(request):
    """ 发布公告 """
    announce = Announce.objects.all()
    import os
    from config.settings import ANNOUNCE_DIR, BASE_DIR

    posts = {}
    errors = []
    succ = False

    if request.method == 'POST':
        posts = {
                'pushTitle' : request.POST.get('pushTitle', ''),
                'pushContent' : request.POST.get('pushContent', ''),
                'pushFbAdd' : request.POST.get('pushFbAdd', ''),
                'pushTid' : int(request.POST.get('pushTid',1)),
                'Apush':    int(request.POST.get('Apush', 0)),
                'LANG':     int(request.POST.get('LANG', 0)),
                'date':    request.POST.get('date', 0),
        }
        if not posts['pushTitle']:
            errors.append("请输入公告标题")
        if not posts['pushContent']:
            errors.append("请输入公告内容")
            if posts['pushTid']==1:
                if not posts['pushFbAdd']:
                    errors.append("请输入facebook公告地址")
        if posts['LANG'] == 0:
            Pcontent = u"活動內容"
            Ptime = u"活動時間"
            Ptitle = u"公告"
        elif posts['LANG'] == 1:
            Pcontent = u"Announce Content"
            Ptime = u"Announce time"
            Ptitle = u"title"
        # facebook公告
        if not errors and posts['pushTid']==1:
            posts['fb'] = 1
            Announce.objects.create(title=posts['pushTitle'],content=posts['pushContent'], \
                facebook=posts['fb'],url=posts['pushFbAdd'], online=1, enddate=posts['date'], \
                language=posts['LANG'])
            succ = True
        # 内部公告
        elif not errors and posts['pushTid']==2:
            posts['fb'] = 0
            Announce.objects.create(title=posts['pushTitle'],content=posts['pushContent'], \
                facebook=posts['fb'], online=1, enddate=posts['date'], language=posts['LANG'])
            id = Announce.objects.latest('id').id
            Announce.objects.filter(id=id).update(url="http://gofree.hk/announce/"+str(id)+".html")
            succ = True
            file_name = str(id)+'.html'
            name = ANNOUNCE_DIR
            file_dir = os.path.join(BASE_DIR, name)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_dir = file_dir + file_name
            html_str = "<!doctype html>\n<html xmlns='http://www.w3.org/1999/xhtml'>\n<head>\n" + \
                "    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>\n" + "    <title>"+Ptitle+"</title>\n" + \
                "    <meta content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no' name='viewport' />\n" + \
                "    <style>\n        * {\n            margin: 0;\n            padding: 0;\n        }\n" + \
                "        img {\n            display: block;\n            max-width: 100%;\n" + \
                "            height: auto;\n            margin: 0 auto;\n        }\n" + "        html, body {\n" + \
                "            background: #fff;\n        }\n" + "        h1 {\n            color: #f82939;\n" + "            font-size: 24px;\n" + \
                "            font-weight: normal;\n" + "            text-align: center;\n" + "            margin: 20px 0 0;\n" + "        }" + \
                "        h1:before {\n" + "            content: '';\n" + "            width: 22px;\n" + "            height: 18px;\n" + \
                "            display: inline-block;\n" + "            background: url(../images/ic_notice.png) no-repeat left center;\n" + \
                "            background-size: 22px 18px;\n" + "            -webkit-background-size: 22px 18px;\n" + \
                "            margin-right: 10px;\n" + "        }" + "        h2 {\n" + "            display: inline-block;\n" + \
                "            color: #fff;\n" + "            background: #f82939;\n" + "            padding: 3px 5px;\n" + \
                "            font-size: 20px;\n" + "            margin-top: 20px;\n" + "            margin-left: 20px;\n" + \
                "            font-weight: normal;\n" + "        }\n" + "        p {\n" + "            color: #1a0406;\n" + \
                "            font-size: 20px;\n" + "            line-height: 30px;\n" + "            margin-top: 10px;\n" + \
                "            margin-left: 32px;\n" + "            margin-right: 20px;\n" + "        }\n" + "    </style>\n" + \
                "</head>\n" + "<body>\n" + "<h1>"+posts['pushTitle']+"</h1>\n"+"<h2>"+Ptime+"</h2>\n" + "<p>" +str(date.today()) +"~"+posts['date'] + "</p>\n" + \
                "<h2>"+Pcontent+"</h2>\n" + "<p>" + posts['pushContent'] + "</p>\n" + "</body>\n" + "</html>"
            with open(file_dir, 'wb') as dest:
                dest.write(html_str.encode('utf-8'))
            succ = True
        # 是否推送
        if not errors and posts['Apush']==1:
            # print 'good'
            pushMsg(posts['pushTitle'])

    return render_to_response('announce/push.html', {
        'title': '公告发布',
        'page_tag': 'announce',
        'username': request.user.username,
        'datas': announce,
        'errors': errors,
        'succ' : succ,
    }, context_instance=RequestContext(request))

def pushMsg(content):
    """推送到Parse"""
    import httplib,json
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
        },
        "data": {
             "alert": ""+content+"",
        }
        }), {
        "X-Parse-Application-Id": "Hi8EGRnR9ng09Z60P2rqhrTjZiT7y7A4UrVmShNG",
        "X-Parse-REST-API-Key": "fX6zQY0EGcGSc3MR4FYp4mViFRTxiGyqTZD6HZdQ",
        "Content-Type": "application/json"
         })


