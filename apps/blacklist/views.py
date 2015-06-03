#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author: lisongjian@youmi.net
#

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from apps.blacklist.models import Iplist, Maillist, Idfalist, Imeilist, Uidlist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.users.models import UserDevices, UserBind

@login_required
def iplist(request):
    """ ip黑名单概况 """
    limit = 25
    orderbyud = orderby = request.GET.get('orderby', 'id')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))

    if not updw:
        orderbyud = '-' + orderby
    datas = Iplist.objects.distinct().order_by(orderbyud)
    if not datas.exists():
        datas = []

    paginator = Paginator(datas, limit)

    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    return render_to_response('blacklist/iplist.html', {
        'title':    'ip黑名单',
        'page_tag': 'blacklist',
        'datas':    datas,
        'orderby':  orderby,
        'updw':     updw,
    })

@login_required
def maillist(request):
    """ mail黑名单概况 """
    limit = 25
    orderbyud = orderby = request.GET.get('orderby', 'id')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))

    if not updw:
        orderbyud = '-' + orderby
    datas = Maillist.objects.order_by(orderbyud)
    if not datas.exists():
        datas = []

    paginator = Paginator(datas, limit)

    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    return render_to_response('blacklist/maillist.html', {
        'title':    'mail黑名单',
        'page_tag': 'blacklist',
        'datas':    datas,
        'orderby':  orderby,
        'updw':     updw,
    })

@login_required
def idfalist(request):
    """ ip黑名单概况 """
    limit = 25
    orderbyud = orderby = request.GET.get('orderby', 'id')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))

    if not updw:
        orderbyud = '-' + orderby
    datas = Idfalist.objects.order_by(orderbyud)
    if not datas.exists():
        datas = []

    paginator = Paginator(datas, limit)

    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    return render_to_response('blacklist/idfalist.html', {
        'title':    'idfa黑名单',
        'page_tag': 'blacklist',
        'datas':    datas,
        'orderby':  orderby,
        'updw':     updw,
    })

@login_required
def imeilist(request):
    """ imei黑名单概况 """
    limit = 25
    orderbyud = orderby = request.GET.get('orderby', 'id')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))

    if not updw:
        orderbyud = '-' + orderby
    datas = Imeilist.objects.order_by(orderbyud)
    if not datas.exists():
        datas = []

    paginator = Paginator(datas, limit)

    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    return render_to_response('blacklist/imeilist.html', {
        'title':    'imei黑名单',
        'page_tag': 'blacklist',
        'datas':    datas,
        'orderby':  orderby,
        'updw':     updw,
    })

@login_required
def uidlist(request):
    """ uid黑名单概况 """
    limit = 25
    orderbyud = orderby = request.GET.get('orderby', 'id')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))

    if not updw:
        orderbyud = '-' + orderby
    datas = Uidlist.objects.order_by(orderbyud)
    if not datas.exists():
        datas = []

    paginator = Paginator(datas, limit)

    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    return render_to_response('blacklist/uidlist.html', {
        'title':    'uid黑名单',
        'page_tag': 'blacklist',
        'datas':    datas,
        'orderby':  orderby,
        'updw':     updw,
    })

@login_required
def ipadd(request):
    """
        =item add  添加商品
    """
    errors = []
    succ = False
    posts = {}
    if request.method == 'POST':
        posts = {
            'ip':   request.POST.get('ip', ''),
            'note':   request.POST.get('note',''),
       }

        # 检查表单值
        if not posts['ip']:
            errors.append('请输入一个IP')
        #if posts['ip']:
        #    ip_info = Iplist.objects.filter(ip=posts['ip']).filter(status=1).values()
        #    if ip_info:
        #        errors.append('IP已存在')
        # 计算消耗钻石
        #posts['exchange_point'] = int(posts['exchange_cost'] * 1000)

        if not errors:
            ip_info = Iplist.objects.filter(ip=posts['ip']).filter(status=1).values()
            if not ip_info:
                Iplist.objects.create(ip=posts['ip'], note=posts['note'],status=1)
            device_info = UserDevices.objects.filter(ip = posts['ip']).values()
            print device_info
            for di in device_info:
                if di['cheat']==0:
                    UserDevices.objects.filter(ip=di['ip']).update(cheat=1, type=1)


            succ = True
            posts = {}  #清空

    datas = Iplist.objects.all()
    if not datas.exists():
        datas = []

    return render_to_response('blacklist/ip_add.html', {
        'title':       '添加黑名单',
        'page_tag':    'blacklist',
        'username':    request.user.username,
        'datas':       datas,
        'errors':      errors,
        'succ':        succ,
        'temps':       posts,
    })

@login_required
def mailadd(request):
    """
        =mail add  添加黑名单
    """
    errors = []
    succ = False
    posts = {}
    if request.method == 'POST':
        posts = {
            'mail':   request.POST.get('mail', ''),
            'note':   request.POST.get('note',''),
       }

        # 检查表单值
        if not posts['mail']:
            errors.append('请输入一个Mail')
        if not errors:
            mail_info = Maillist.objects.filter(mail=posts['mail']).filter(status=1).values()
            if not mail_info:
                Maillist.objects.create(mail=posts['mail'], note=posts['note'],status=1)

            succ = True
            posts = {}  #清空

    datas = Maillist.objects.all()
    if not datas.exists():
        datas = []

    return render_to_response('blacklist/mail_add.html', {
        'title':       '添加黑名单',
        'page_tag':    'blacklist',
        'username':    request.user.username,
        'datas':       datas,
        'errors':      errors,
        'succ':        succ,
        'temps':       posts,
    })

@login_required
def imeiadd(request):
    """
        =imei add
    """
    errors = []
    succ = False
    posts = {}
    if request.method == 'POST':
        posts = {
            'imei':   request.POST.get('imei', ''),
            'note':   request.POST.get('note',''),
       }

        # 检查表单值
        if not posts['imei']:
            errors.append('请输入一个imei')
        if not errors:
            imei_info = Imeilist.objects.filter(imei=posts['imei']).filter(status=1).values()
            if not imei_info:
                Imeilist.objects.create(imei=posts['imei'], note=posts['note'],status=1)
            device_info = UserDevices.objects.filter(ei = posts['imei']).values()
            for di in device_info:
                if di['cheat']==0:
                    UserDevices.objects.filter(ei=di['ei']).update(cheat=1, type=2)
            succ = True
            posts = {}  #清空

    datas = Imeilist.objects.all()
    if not datas.exists():
        datas = []

    return render_to_response('blacklist/imei_add.html', {
        'title':       '添加黑名单',
        'page_tag':    'blacklist',
        'username':    request.user.username,
        'datas':       datas,
        'errors':      errors,
        'succ':        succ,
        'temps':       posts,
    })

@login_required
def idfaadd(request):
    """
        =idfa add  添加黑名单
    """
    errors = []
    succ = False
    posts = {}
    if request.method == 'POST':
        posts = {
            'idfa':   request.POST.get('idfa', ''),
            'note':   request.POST.get('note',''),
        }

        # 检查表单值
        if not posts['idfa']:
            errors.append('请输入一个idfa')
        if not errors:
            idfa_info = Idfalist.objects.filter(idfa=posts['idfa']).filter(status=1).values()
            if not idfa_info:
                Idfalist.objects.create(idfa=posts['idfa'], note=posts['note'],status=1)
            device_info = UserDevices.objects.filter(idfa = posts['idfa']).values()
            for di in device_info:
                if di['cheat']==0:
                    UserDevices.objects.filter(idfa=di['idfa']).update(cheat=1, type=3)
            succ = True
            posts = {}  #清空

    datas = Idfalist.objects.all()
    if not datas.exists():
        datas = []

    return render_to_response('blacklist/idfa_add.html', {
        'title':       '添加黑名单',
        'page_tag':    'blacklist',
        'username':    request.user.username,
        'datas':       datas,
        'errors':      errors,
        'succ':        succ,
        'temps':       posts,
    })


@login_required
def uidadd(request):
    """
        =uid add  添加黑名单
    """
    errors = []
    succ = False
    posts = {}
    if request.method == 'POST':
        posts = {
            'uid':   request.POST.get('uid', ''),
            'note':   request.POST.get('note',''),
       }

        # 检查表单值
        if not posts['uid']:
            errors.append('请输入一个uid')
        if not errors:
            blackUser = Uidlist.objects.distinct().filter(uid=posts['uid']).filter(status=1).values()
            if not blackUser:
                Uidlist.objects.create(uid=posts['uid'], status=1)
            userbind = UserBind.objects.values('token').distinct().filter(uid = posts['uid'])
            for ub in userbind:
                device_info = UserDevices.objects.filter(fingerprinting = ub['token']).values()
                for di in device_info:
                    blackUser = Uidlist.objects.distinct().filter(uid=posts['uid']).filter(status=1).values()
                    ip_info = Iplist.objects.filter(ip=di['ip']).filter(status=1).values()
                    imei_info = Imeilist.objects.filter(imei=di['ei']).filter(status=1).values()
                    idfa_info = Idfalist.objects.filter(idfa=di['idfa']).filter(status=1).values()
                    blackUser = Uidlist.objects.distinct().filter(uid=posts['uid']).filter(status=1).values()
                    if not blackUser:
                        Uidlist.objects.create(uid=posts['uid'], status=1)
                    if not ip_info and di['ip']!=None:
                        Iplist.objects.create(ip=di['ip'], note=posts['uid'], status=1)
                    if not imei_info and di['ei']!=None:
                        Imeilist.objects.create(imei=di['ei'], note=posts['uid'], status=1)
                    if not idfa_info and di['idfa']!=None:
                        Idfalist.objects.create(idfa=di['idfa'], note=posts['uid'], status=1)
        succ = True
        posts = {}  #清空

    datas = Uidlist.objects.all()
    if not datas.exists():
        datas = []

    return render_to_response('blacklist/uid_add.html', {
        'title':       '添加黑名单',
        'page_tag':    'blacklist',
        'username':    request.user.username,
        'datas':       datas,
        'errors':      errors,
        'succ':        succ,
        'temps':       posts,
    })


