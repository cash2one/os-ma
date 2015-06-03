#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from apps.setting.models import AdConfig, Options, Recommend, Feedback, Daily
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from apps.users.models import Users
import httplib,json


@login_required
def adconfig(request):
    """ 广告配置 """
    datas = AdConfig.objects.all().order_by('-aos_status', '-ios_status')
    if not datas.exists():
        datas = []

    return render_to_response('setting/adconfig.html', {
        'title': '广告配置',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas': datas,
    })


@login_required
def ad_edit(request):
    """ 修改广告配置 """
    errors = []
    succ = False
    ad_id = 0
    if request.method == 'GET':
        ad_id = request.GET.get('ad_id', 0)
        if ad_id:
            datas = AdConfig.objects.get(ad_id=ad_id)
        else:
            return None
    elif request.method == 'POST':
        datas = {
            'ad_id':        int(request.POST.get('ad_id', 0)),
            'description':  request.POST.get('description', ''),
            'title':        request.POST.get('title', ''),
            'intro':        request.POST.get('intro', ''),
            'detail':       request.POST.get('intro', ''),
            'credits':      request.POST.get('credits',''),
            'exchangeRate': float(request.POST.get('exchangeRate',100)),
            'icon':         request.POST.get('icon', ''),
            'aos_status':   int(request.POST.get('aos_status', 1)),
            'ios_status':   int(request.POST.get('ios_status', 1)),
            'priority':     int(request.POST.get('priority', 0)),
            'iospriority':     int(request.POST.get('iospriority', 0)),
            'pname':        request.POST.get('pname', ''),

        }
        if datas['ad_id']:
            if not datas['description']:
                errors.append('请输入广告渠道名称')
            if not datas['title']:
                errors.append('请输入广告渠道别名')
            if not datas['intro']:
                errors.append('请输入广告渠道简称')
            if not datas['detail']:
                errors.append('请输入广告详细介绍')
            if not datas['credits']:
                errors.append('请输入积分数')
            if not datas['exchangeRate']:
                errors.append('请输入兑换比例')
            if not datas['icon']:
                errors.append('请输入图标颜色')
        else:
            return None

        if not errors:
            AdConfig.objects.filter(ad_id=datas['ad_id']).update(
                description=datas['description'], title=datas['title'],
                intro=datas['intro'], detail=datas['detail'],credits=datas['credits'],
                icon=datas['icon'], aos_status=datas['aos_status'],exchangeRate=datas['exchangeRate'],
                ios_status=datas['ios_status'], priority=datas['priority'], iospriority=datas['iospriority'],
                pname = datas['pname'])

            succ = True

    else:
        return None

    return render_to_response('setting/ad_edit.html', {
        'title': '编辑广告配置',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas': datas,
        'succ': succ,
        'errors': errors,
    })


@login_required
def ad_add(request):
    """ 添加广告配置 """
    pass


@login_required
def ad_del(request):
    """ 删除广告配置 """
    res = {'c': -1}
    ad_id = request.GET.get('ad_id', None)
    if ad_id:
        AdConfig.objects.get(ad_id=ad_id).delete()
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")


@login_required
def options(request):
    """ 参数配置 """
    options = Options.objects.all()
    return render_to_response('setting/options.html', {
        'title': '参数配置',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas': options,
    })


@login_required
def opt_edit(request):
    """ 参数配置修改 """
    errors = []
    succ = False
    if request.method == 'GET':
        id = request.GET.get('id', 0)
        if id:
            datas = Options.objects.get(id=id)
        else:
            return None
    elif request.method == 'POST':
        datas = {
            'id':           int(request.POST.get('id', 0)),
            'values':       request.POST.get('values', 0),
            'description':  request.POST.get('description', ''),
            'key':          request.POST.get('key', ''),
        }
        if datas['id']:
            if not datas['values']:
                errors.append('请输入参数值')
            if not datas['description']:
                errors.append('请输入说明文字')
        else:
            return None

        if not errors:
            Options.objects.filter(id=datas['id']).update(
                description=datas['description'], values=int(datas['values']))

            succ = True

    else:
        return None

    return render_to_response('setting/opt_edit.html', {
        'title': '参数配置修改',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas': datas,
        'succ': succ,
        'errors': errors,
    })

@login_required
def daily(request):
    """ 每日奖励设置 """
    daily = Daily.objects.all()
    return render_to_response('setting/daily.html', {
        'title': '每日奖励',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas': daily,
    })


@login_required
def day_edit(request):
    """ 每日奖励修改 """
    errors = []
    succ = False
    if request.method == 'GET':
        id = request.GET.get('id', 0)
        if id:
            datas = Daily.objects.get(id=id)
        else:
            return None
    elif request.method == 'POST':
        datas = {
            'id':           int(request.POST.get('id', 0)),
            'ad_id':        request.POST.get('ad_id', 0),
            'description':  request.POST.get('description', ''),
            'title':        request.POST.get('title', ''),
            'total_task':   int(request.POST.get('total_task', '')),
            'points':       int(request.POST.get('points', '')),
            'status':       int(request.POST.get('status', 0)),
       }
        if datas['id']:
            if not datas['description']:
                errors.append('请输入说明文字')
            if not datas['ad_id']:
                errors.append('请输入广告平台id')
            if not datas['title']:
                errors.append('请输入广告标题')
            if not datas['total_task']:
                errors.append('请输入完成任务数')
            if not datas['points']:
                errors.append('请输入奖励点数')
        else:
            return None

        if not errors:
            Daily.objects.filter(id=datas['id']).update(
                description=datas['description'], ad_id=int(datas['ad_id']), \
                title=datas['title'], total_task=datas['total_task'], \
                points=datas['points'],status=datas['status'])

            succ = True

    else:
        return None

    return render_to_response('setting/day_edit.html', {
        'title': '每日奖励修改',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas': datas,
        'succ': succ,
        'errors': errors,
    })

@login_required
def recommend(request):
    """ 帮抢高价 """
    recommend = Recommend.objects.all()
    return render_to_response('setting/recommend.html', {
        'title': '帮抢高价',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas': recommend,
    })

@login_required
def re_edit(request):
    """ 修改帮抢高价任务 """
    errors = []
    succ = False
    id = 0
    if request.method == 'GET':
        id = request.GET.get('id', 0)
        if id:
            datas = Recommend.objects.get(id=id)
        else:
            return None
    elif request.method == 'POST':
        datas = {
            'id':           int(request.POST.get('id', 0)),
            'title':       request.POST.get('title', ''),
            'description':  request.POST.get('description', ''),
            'points':       request.POST.get('points', 0),
            'status':       int(request.POST.get('status', 1)),
            'ad_id':        int(request.POST.get('ad_id', 1)),
        }
        if datas['id']:
            if not datas['title']:
                errors.append('请输入任务标题')
            if not datas['description']:
                errors.append('请输入任务详细描述')
            if not datas['points']:
                errors.append('请输入任务积分数')
        else:
            return None

        if not errors:
            Recommend.objects.filter(id=datas['id']).update(
                description=datas['description'], title=datas['title'],
                points=datas['points'], status=datas['status'], ad_id=datas['ad_id'])

            succ = True

    else:
        return None

    adconfig = AdConfig.objects.filter(aos_status=1)
    return render_to_response('setting/re_edit.html', {
        'title': '编辑任务',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas': datas,
        'ad': adconfig,
        'succ': succ,
        'errors': errors,
    })


@login_required
def re_del(request):
    """ 删除任务 """
    res = {'c': -1}
    id = request.GET.get('id', None)
    if id:
        Recommend.objects.get(id=id).delete()
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def re_add(request):
    """ 添加任务 """
    errors = []
    succ = False
    datas = {
        'status': 1,
        'ad_id': 1,
    }
    if request.method == 'POST':
        datas = {
            'title':       request.POST.get('title', ''),
            'description':  request.POST.get('description', ''),
            'points':       request.POST.get('points', 0),
            'status':       int(request.POST.get('status', 1)),
            'ad_id':        int(request.POST.get('ad_id', 1)),
        }
        if not datas['title']:
            errors.append('请输入任务标题')
        if not datas['description']:
            errors.append('请输入任务详细描述')
        if not datas['points']:
            errors.append('请输入任务积分数')

        if not errors:
            Recommend.objects.create(
                title=datas['title'], description=datas['description'],
                points=datas['points'], status=datas['status'], ad_id=datas['ad_id'])

            succ = True

    adconfig = AdConfig.objects.filter(aos_status=1)
    if not adconfig:
        adconfig = []

    return render_to_response('setting/re_add.html', {
        'title': '编辑任务',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas': datas,
        'ad': adconfig,
        'succ': succ,
        'errors': errors,
    })

@login_required
def feedback(request):
    """ 反馈信息概况 """
    limit = 25
    #orderbyud = orderby = request.GET.get('orderby', 'id')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))

    # if not updw:
    #    orderbyud = '-' + orderby
    datas = Feedback.objects.order_by('-status').reverse()
    if not datas.exists():
        datas = []

    paginator = Paginator(datas, limit)

    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    return render_to_response('setting/feedback.html', {
        'title':    '反馈信息',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas':    datas,
        # 'orderby':  orderby,
        'updw':     updw,
    })

@login_required
def deal(request):
    """
        =处理留言
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认删除
    if gid:
        feedback = Feedback.objects.get(id=gid)
	feedback.status=1
	feedback.save()
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def push(request):
    """
        = 添加push通知
    """
    import os
    import Image
    from config.settings import PUSH_DIR, BASE_DIR


    posts = {}
    errors = []
    succ = False

    #sw = 72
    #sh = 72

    if request.method == 'POST':
        #获取前台传过来的新增商品类型信息
        file_obj = request.FILES.get('pushIcon', None)
        posts = {
                'pushTitle' : request.POST.get('pushTitle', ''),
                'pushContent' : request.POST.get('pushContent', ''),
                'pushVersion' : request.POST.get('pushVersion', ''),
                'pushTid' : int(request.POST.get('pushTid',0)),
                'scopeid' : request.POST.get('scopeid',''),
        }
        if posts['pushTid']==4:
            if not file_obj:
                errors.append("请选择推送图片")
               #if width > sw or height > sh:
                #    errors.append("图标规格不正确，请选择至多72*72的图标上传")
            if not posts['pushTitle']:
                errors.append("请输入推送标题")
            if not posts['pushContent']:
                errors.append("请输入推送内容")
        if not errors and posts['pushTid']==4:
            image = Image.open(file_obj)
            (width, height) = image.size
            file_name = file_obj.name
            name = PUSH_DIR
            file_dir = os.path.join(BASE_DIR, name)
            print file_dir
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_dir = file_dir + file_name
            posts['pushIcon'] = 'push/'+file_name
            with open(file_dir, 'wb') as dest:
                for chunk in file_obj.chunks():
                    dest.write(chunk)
            pushDiy(posts['pushTitle'],posts['pushContent'],file_name)
            pushDiyVersiontest(posts['pushTitle'],posts['pushContent'],file_name)
            succ = True
        elif posts['pushTid']==3:
            if not posts['pushContent']:
                errors.append("请输入推送内容")
            if not posts['pushVersion']:
                errors.append("请输入推送版本")
            if not errors:
                pushNewVersion(posts['pushContent'],posts['pushVersion'])
                pushNewVersiontest(posts['pushContent'],posts['pushVersion'])
                succ = True
        elif posts['pushTid']==2:
            if not posts['pushContent']:
                errors.append("请输入推送内容")
            if not errors:
                pushMsg(posts['pushContent'])
                #pushMsgVersiontest(posts['pushContent'])
                succ = True
        elif posts['pushTid']==5:
            if not posts['pushContent']:
                errors.append("请输入推送长消息")
            if not errors:
                pushLongMsg(posts['pushContent'])
                #pushMsgVersiontest(posts['pushContent'])
                succ = True
        elif posts['pushTid']==1:
            if not posts['pushContent']:
                errors.append("请输入推送内容")
            if not errors:
                pushKakaMsg(posts['pushContent'])
                succ = True
        elif posts['pushTid']==6:
            if not posts['pushContent']:
                errors.append("请输入推送长消息")
            if not errors:
                pushKakaLongMsg(posts['pushContent'])
                #pushMsgVersiontest(posts['pushContent'])
                succ = True
        elif posts['pushTid']==7:
            if not posts['pushContent']:
                errors.append("请输入推送消息")
            #if not posts['scopeid']:
            print posts

            if not errors:
                user = get_object_or_404(Users, uid=posts['scopeid'])
                scopeid = user.scopeid
                pushScopeid(scopeid,posts['pushContent'])
                succ = True

    return render_to_response('setting/push.html', {
            'title' : '推送通知',
            'page_tag' : 'setting',
            'username' : request.user.username,
            'errors' : errors,
            'succ' : succ,
        })

def pushDiy(title,content,pic):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
             "appVersion": { "$regex": "^\\Q1.3.1.4\\E"}
        },
        "data": {
             "action": "4",
             "pop": "0",
             "data":{
                    "icon": "http://www.gofree.hk/push/"+pic+"",
                    #"icon": "http://www.baidu.com/img/baidu_jgylogo3.gif",
                    "title": ""+title+"",
                    "content": ""+content+"",
                    "flag": "0",
        }
        }
        }), {
        "X-Parse-Application-Id": "Hi8EGRnR9ng09Z60P2rqhrTjZiT7y7A4UrVmShNG",
        "X-Parse-REST-API-Key": "fX6zQY0EGcGSc3MR4FYp4mViFRTxiGyqTZD6HZdQ",
        "Content-Type": "application/json"
         })

def pushNewVersion(content,version):
    """推送到Parse"""
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
             "appVersion": { "$ne": ""+version+""},
        },
        "data": {
             "action": 3,
             "alert": ""+content+"",
        }
        }), {
        "X-Parse-Application-Id": "Hi8EGRnR9ng09Z60P2rqhrTjZiT7y7A4UrVmShNG",
        "X-Parse-REST-API-Key": "fX6zQY0EGcGSc3MR4FYp4mViFRTxiGyqTZD6HZdQ",
        "Content-Type": "application/json"
         })

def pushMsg(content):
    """推送到Parse"""
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
            # "scopeid": "315170755336015"
       },
        "data": {
             "alert": ""+content+"",
        }
        }), {
        "X-Parse-Application-Id": "Hi8EGRnR9ng09Z60P2rqhrTjZiT7y7A4UrVmShNG",
        "X-Parse-REST-API-Key": "fX6zQY0EGcGSc3MR4FYp4mViFRTxiGyqTZD6HZdQ",
        "Content-Type": "application/json"
         })

def pushDiyVersiontest(title,content,pic):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
             "appVersion": { "$regex": "^\\Q1.3.1.4\\E"}
        },
        "data": {
             "action": "4",
             "pop": "0",
             "data":{
                    "icon": "http://www.gofree.hk/push/"+pic+"",
                    #"icon": "http://www.baidu.com/img/baidu_jgylogo3.gif",
                    "title": ""+title+"",
                    "content": ""+content+"",
                    "flag": "0",
        }
        }
        }), {
        "X-Parse-Application-Id": "qAnqJOboJ72vtvnfy7bxg4fIraIrW5IukJLUMJdZ",
        "X-Parse-REST-API-Key": "jy9ksVv6gJMWLTk9ir0okVc2fEPzXafUdsvI4QTZ",
        "Content-Type": "application/json"
         })
def pushNewVersiontest(content,version):
    """推送新版本"""
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
             "appVersion": { "$ne": ""+version+""},
        },
        "data": {
             "action": 3,
             "alert": ""+content+"",
        }
        }), {
        "X-Parse-Application-Id": "qAnqJOboJ72vtvnfy7bxg4fIraIrW5IukJLUMJdZ",
        "X-Parse-REST-API-Key": "jy9ksVv6gJMWLTk9ir0okVc2fEPzXafUdsvI4QTZ",
        "Content-Type": "application/json"
         })
def pushMsgVersiontest(content):
    """推送信息"""
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
            # "scopeid": "315170755336015"
        },
        "data": {
             "alert": ""+content+"",
        }
        }), {
        "X-Parse-Application-Id": "qAnqJOboJ72vtvnfy7bxg4fIraIrW5IukJLUMJdZ",
        "X-Parse-REST-API-Key": "jy9ksVv6gJMWLTk9ir0okVc2fEPzXafUdsvI4QTZ",
        "Content-Type": "application/json"
         })
def pushKakaMsg(content):
    """推送到kaka"""
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
             #"scopeid": "324479581071799"
        },
        "data": {
             "alert": ""+content+"",
        }
        }), {
        "X-Parse-Application-Id": "qG4ld59rAS57sLBb6pAuYAZRyjrAUR1KFWLLeMRN",
        "X-Parse-REST-API-Key": "CN69v4Rp9peSZYzzyjqa8fsGxqbvjp74FJit9o5j",
        "Content-Type": "application/json"
         })

def pushLongMsg(content):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
        },
        "data": {
             "action": "5",
             "pop": "0",
             "data":{
                    "content": ""+content+"",
                    "flag": "0",
        }
        }
        }), {
        "X-Parse-Application-Id": "Hi8EGRnR9ng09Z60P2rqhrTjZiT7y7A4UrVmShNG",
        "X-Parse-REST-API-Key": "fX6zQY0EGcGSc3MR4FYp4mViFRTxiGyqTZD6HZdQ",
        "Content-Type": "application/json"
         })

def pushKakaLongMsg(content):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
        },
        "data": {
             "action": "5",
             "pop": "0",
             "data":{
                    "content": ""+content+"",
                    "flag": "0",
        }
        }
        }), {
        "X-Parse-Application-Id": "qG4ld59rAS57sLBb6pAuYAZRyjrAUR1KFWLLeMRN",
        "X-Parse-REST-API-Key": "CN69v4Rp9peSZYzzyjqa8fsGxqbvjp74FJit9o5j",
        "Content-Type": "application/json"
         })

def pushScopeid(scopeid,title):
    """推送到Parse"""
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
             "scopeid": ""+scopeid+""
        },
        "data": {
             "action": 1,
             "alert": title.encode("utf-8")
        }
        }), {
        "X-Parse-Application-Id": "Hi8EGRnR9ng09Z60P2rqhrTjZiT7y7A4UrVmShNG",
        "X-Parse-REST-API-Key": "fX6zQY0EGcGSc3MR4FYp4mViFRTxiGyqTZD6HZdQ",
        "Content-Type": "application/json"
         })

