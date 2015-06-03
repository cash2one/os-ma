#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author chenjiehua@youmi.net,lisongjian@youmi.net
#

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.users.models import Users, GlobalOrders, UserDevices, UserBind, CallbackOrders, appList
from apps.blacklist.models import Iplist, Idfalist, Imeilist, Uidlist
from apps.setting.models import Options
from django.http import HttpResponse
from apps.converts.models import ExchangeOrders
import logging, json
import IP
from datetime import datetime, timedelta

@login_required
def index(request, gid=0):
    """ 用户信息概况 """
    limit = 25
    orderbyud = orderby = request.GET.get('orderby', 'uid')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))
    gid = int(gid)
    cur_app = {}
    cur_app['gid'] = gid
    applist = appList.objects.order_by('-id')
    date = request.GET.get('date')
    enddate = request.GET.get('enddate')
    if not date:
        date_start = datetime.strftime(datetime.now(), "%Y-%m-01")
        date_end = datetime.strftime(datetime.now()+timedelta(days=1), "%Y-%m-%d")
    else:
        date_start = date
        date_end = enddate
    if not updw:
        orderbyud = '-' + orderby
    for a in applist:
        if a.id == gid:
            cur_app['title'] = a.name
    if not gid:
        cur_app['title'] = '全部'
        users = Users.objects.filter(create_at__gte=date_start, create_at__lt=date_end).order_by(orderbyud)

    if gid:
        if gid == 1:
            users = Users.objects.filter(create_at__gte=date_start, create_at__lt=date_end, platform = 2).order_by(orderbyud)
        elif gid ==2:
            users = Users.objects.filter(create_at__gte=date_start, create_at__lt=date_end, platform = 1).order_by(orderbyud)
        elif gid ==3:
            users = Users.objects.filter(create_at__gte=date_start, create_at__lt=date_end, appType = 0).order_by(orderbyud)
        elif gid ==4:
            users = Users.objects.filter(create_at__gte=date_start, create_at__lt=date_end, appType =1).order_by(orderbyud)
        elif gid ==5:
            users = Users.objects.filter(create_at__gte=date_start, create_at__lt=date_end, en =1).order_by(orderbyud)
    count = users.count()
    #if not users.exists():
    #    users = []
    paginator = Paginator(users, limit)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render_to_response('users/index.html', {
        'title':    '用户信息',
        'page_tag': 'users',
        'username': request.user.username,
        'datas':    users,
        'orderby':  orderby,
        'updw':     updw,
        'applist':    applist,
        'cur_app': cur_app,
        'count': count,
        'query_date': date_start,
        'query_enddate': date_end,
    })


@login_required
def search(request):
    """ 搜索 """
    uid = request.GET.get('uid')
    ad_from = request.GET.get('ad_from')
    utm_source = request.GET.get('utm_source')
    scopeid = request.GET.get('scopeid')
    invited_code =request.GET.get('invited_code')
    page = int(request.GET.get('page', 1))
    limit = 25
    flag = True
    total = 0
    params = {}
    if uid:
        params.setdefault('uid', uid)
        flag = False
    if ad_from:
        params.setdefault('ad_from', ad_from)
        flag = False
    if utm_source:
        params.setdefault('utm_source', utm_source)
        flag = False
    if scopeid:
        params.setdefault('scopeid', scopeid)
        flag = False
    if invited_code:
        params.setdefault('invited_code', invited_code)
        flag = False
    if not flag:
        users = Users.objects.filter(**params).order_by('create_at').reverse()
        total = users.count()
    else:
        users = None
    paginator = Paginator(users, limit)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render_to_response('users/search.html', {
        'title': '搜索结果',
        'page_tag': 'users',
        'username': request.user.username,
        'datas': users,
        'ad_from': ad_from,
        'uid': uid,
        'scopeid': scopeid,
        'invited_code': invited_code,
        'utm_source': utm_source,
        'total': total,
    })


@login_required
def user_exchange(request, uid):
    """ 用户已兑换积分情况 """
    ex_order = ExchangeOrders.objects.filter(uid=uid).order_by('-oid')
    if not ex_order.exists():
        ex_order = []

    return render_to_response('users/user_ex.html', {
        'title': '用户已兑换积分',
        'page_tag': 'users',
        'username': request.user.username,
        'datas': ex_order,
        'uid': uid,
    })


@login_required
def user_invite(request, uid):
    """ 用户邀请所得积分情况 """
    pass


@login_required
def user_detail(request, uid, page=1):
    """ 用户所有积分情况 """
    datas = []
    user = get_object_or_404(Users, uid=uid)
    import urllib,urllib2, os
    from config.settings import BASE_DIR, USER_DIR
    options = get_object_or_404(Options, id=32)
    if options.values == 1:
        url = "http://graph.facebook.com/"+user.scopeid+"/picture?type=small"
        u = urllib2.urlopen(url)
        realUrl = u.geturl()
        image = urllib.URLopener()
        file_dir = os.path.join(BASE_DIR, USER_DIR)
        image.retrieve(realUrl,file_dir+user.scopeid+'.jpg')
    userdevices = []
    device_info = []
    ipadd = ''
    if user.ip:
        ipadd = IP.find(user.ip)
    orders = GlobalOrders.objects.filter(uid=uid).order_by('-record_time')
    userbind = UserBind.objects.values('token').distinct().filter(uid = uid)
    blackUser = Uidlist.objects.distinct().filter(uid=uid).values()
    #if blackUser:
    #    Users.objects.filter(uid=uid).update(wonder=1)
    user = get_object_or_404(Users, uid=uid)
    count = 0
    aos = 0
    ios = 0
    for ub in userbind:
        device_info = UserDevices.objects.distinct().filter(fingerprinting = ub['token']).values()
        for di in device_info:
            ip_info = Iplist.objects.filter(ip=di['ip']).filter(status=1).values()
            imei_info = Imeilist.objects.filter(imei=di['ei']).filter(status=1).values()
            idfa_info = Idfalist.objects.filter(idfa=di['idfa']).filter(status=1).values()
            #if ip_info or imei_info or idfa_info:
            #    Users.objects.filter(uid=uid).update(wonder=1)
            if ip_info:
                UserDevices.objects.filter(ip=di['ip']).update(cheat=1, type=1)
                if not blackUser:
                    Uidlist.objects.filter(uid=uid).create(uid=uid, note='ip', status=1)
            elif imei_info:
                UserDevices.objects.filter(ei=di['ei']).update(cheat=1, type=2)
                if not blackUser:
                    Uidlist.objects.filter(uid=uid).create(uid=uid, note='ip', status=1)
            elif idfa_info:
                UserDevices.objects.filter(idfa=di['idfa']).update(cheat=1, type=3)
                if not blackUser:
                    Uidlist.objects.filter(uid=uid).create(uid=uid, note='ip', status=1)
            elif di['idfa'] and not di['ei']:
                ios = 2
            elif di['ei'] and not di['idfa']:
                aos = 1
        count = aos + ios
        device_infoUpdate = UserDevices.objects.distinct().filter(fingerprinting = ub['token']).values()
        for di in device_infoUpdate:
            userdevices.append(di)
            logging.info(userdevices)
            #print count
    #print userdevices
    # 分页
    limit = 50
    page = int(page)
    paginator = Paginator(orders, limit)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    return render_to_response('users/user_detail.html', {
        'title': '用户积分详账',
        'page_tag': 'users',
        'username': request.user.username,
        'datas': datas,
        'uid': uid,
        'user': user,
        'userdevices': userdevices,
        'count': count,
        'ip': ipadd,
    })

@login_required
def user_edit(request):
    """ 用户积分修改 """
    errors = []
    succ = False
    if request.method == 'GET':
        uid = request.GET.get('uid', 0)
        if uid:
            datas = Users.objects.get(uid=uid)
        else:
            return None
    elif request.method == 'POST':
        datas = {
            'uid':           int(request.POST.get('uid', 0)),
            'points':       request.POST.get('points', 0),
            'addpoints':       request.POST.get('addpoints', 0),
            'note':       request.POST.get('note', ''),
            # 'star_gg':   int(request.POST.get('star_gg', 0)),
        }
        if datas['uid']:
            if not datas['addpoints']:
                errors.append('请输入用户积分')
        else:
            return None
        if not errors:
            '''
            if datas['star_gg'] == 1:
                Users.objects.filter(uid=datas['uid']).update(star_gg=1, points=(int(datas['points'])+int(datas['addpoints'])))
                p = GlobalOrders.objects.create(uid=datas['uid'], type='10', note="GooglePlay五星好評", \
                    last=datas['points'], points=int(datas['addpoints']))
                CallbackOrders.objects.create(order=datas['note'], ad_source='10', platform=3, ad="GooglePlay五星好評", \
                    user=datas['uid'], points=int(datas['addpoints']))
            '''
            Users.objects.filter(uid=datas['uid']).update(points=(int(datas['points'])+int(datas['addpoints'])))
            GlobalOrders.objects.create(uid=datas['uid'], type='9', note=datas['note'], \
                last=datas['points'], points=int(datas['addpoints']))
            CallbackOrders.objects.create(order=datas['note'], ad_source='9', platform=3, ad=datas['note'], \
                user=datas['uid'], points=int(datas['addpoints']))
        succ = True
    else:
        return None
    return render_to_response('users/user_edit.html', {
        'title': '用户积分修改',
        'page_tag': 'setting',
        'username': request.user.username,
        'datas': datas,
        'succ': succ,
        'errors': errors,
    })

@login_required
def usersdetailBlack(request):
    """
        =一键黑名单
    """
    res = { 'c': -1 }
    uid = request.GET.get('uid', None)
    # 确认
    if uid:
        userbind = UserBind.objects.values('token').distinct().filter(uid = uid)
        user = get_object_or_404(Users, uid=uid)
        blackUser = Uidlist.objects.distinct().filter(uid=uid).filter(status=1).values()
        if not blackUser:
            blackUser2 = Uidlist.objects.distinct().filter(uid=uid).filter(status=0).values()
            if blackUser2:
                Uidlist.objects.filter(uid=uid).update(uid=uid, note='一键黑名单', status=1)
            else:
                Uidlist.objects.filter(uid=uid).create(uid=uid, note='一键黑名单', status=1)
        ip_info = Iplist.objects.filter(ip=user.ip).filter(status=1).values()
        if not ip_info:
            ip_info2 = Iplist.objects.filter(ip=user.ip).filter(status=0).values()
            if ip_info2:
                Iplist.objects.filter(ip=user.ip).update(ip=user.ip, note='一键黑名单'+str(uid), status=1)
            else:
                if user.ip != None:
                    Iplist.objects.create(ip=user.ip, note='一键黑名单'+str(uid), status=1)
        for ub in userbind:
            device_info = UserDevices.objects.filter(fingerprinting = ub['token']).values()
            for di in device_info:
                imei_info = Imeilist.objects.filter(imei=di['ei']).filter(status=1).values()
                idfa_info = Idfalist.objects.filter(idfa=di['idfa']).filter(status=1).values()
                imei_info2 = Imeilist.objects.filter(imei=di['ei']).filter(status=0).values()
                idfa_info2 = Idfalist.objects.filter(idfa=di['idfa']).filter(status=0).values()
                if not blackUser:
                    if blackUser2:
                        Uidlist.objects.filter(uid=uid).update(uid=uid, note='一键黑名单', status=1)
                    else:
                        Uidlist.objects.filter(uid=uid).create(uid=uid, note='一键黑名单', status=1)
                if not ip_info and di['ip']!=None:
                    if ip_info2:
                        Iplist.objects.filter(ip=di['ip']).update(ip=di['ip'], note='一键黑名单'+str(uid), status=1)
                    else:
                        Iplist.objects.create(ip=di['ip'], note='一键黑名单'+str(uid), status=1)
                if not imei_info and di['ei']!=None:
                    if imei_info2:
                        Imeilist.objects.filter(imei=di['ei']).update(imei=di['ei'], note='一键黑名单'+str(uid), status=1)
                    else:
                        Imeilist.objects.create(imei=di['ei'], note='一键黑名单'+str(uid), status=1)
                if not idfa_info and di['idfa']!=None:
                    if idfa_info2:
                        Idfalist.objects.filter(idfa=di['idfa']).update(idfa=di['idfa'], note='一键黑名单'+str(uid), status=1)
                    else:
                        Idfalist.objects.create(idfa=di['idfa'], note='一键黑名单'+str(uid), status=1)
        return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def usersdetailBlank(request):
    """
        =一键白名单
    """
    res = { 'c': -1 }
    uid = request.GET.get('uid', None)
    # 确认
    if uid:
        userbind = UserBind.objects.values('token').distinct().filter(uid = uid)
        user = get_object_or_404(Users, uid=uid)
        blackUser = Uidlist.objects.distinct().filter(uid=uid).filter(status=1).values()
        if blackUser:
            Uidlist.objects.filter(uid=uid).update(uid=uid, note='一键白名单', status=0)
        ip_info = Iplist.objects.filter(ip=user.ip).filter(status=1).values()
        if ip_info:
            Iplist.objects.filter(ip=user.ip).update(ip=user.ip, note='一键白名单'+str(uid), status=0)
        for ub in userbind:
            device_info = UserDevices.objects.filter(fingerprinting = ub['token']).values()
            UserDevices.objects.filter(fingerprinting = ub['token']).update(cheat=0,type=0)
            for di in device_info:
                blackUser = Uidlist.objects.distinct().filter(uid=uid).filter(status=1).values()
                ip_info = Iplist.objects.filter(ip=di['ip']).filter(status=1).values()
                imei_info = Imeilist.objects.filter(imei=di['ei']).filter(status=1).values()
                idfa_info = Idfalist.objects.filter(idfa=di['idfa']).filter(status=1).values()
                if blackUser:
                    Uidlist.objects.filter(uid=uid).update(uid=uid, note='一键白名单', status=0)
                if ip_info:
                    Iplist.objects.filter(ip=di['ip']).update(ip=di['ip'], note='一键白名单'+str(uid), status=0)
                if imei_info:
                    Imeilist.objects.filter(imei=di['ei']).update(imei=di['ei'], note='一键白名单'+str(uid), status=0)
                if idfa_info:
                    Idfalist.objects.filter(idfa=di['idfa']).update(idfa=di['idfa'], note='一键白名单'+str(uid), status=0)
        return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def wonder(request):
    """
        =怀疑
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认
    if gid:
        ExchangeOrders.objects.filter(uid=gid).update(wonder=1)
        user = Users.objects.get(uid=gid)
        user.wonder=1
        user.save(update_fields=['wonder'])
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def nowonder(request):
    """
        =取消怀疑
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认
    if gid:
        ExchangeOrders.objects.filter(uid=gid).update(wonder=0)
        user = Users.objects.get(uid=gid)
        user.wonder=0
        user.save(update_fields=['wonder'])
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")
