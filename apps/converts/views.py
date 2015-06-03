#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author chenjiehua@youmi.net
#

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from apps.converts.models import ExchangeOrders, ExchangeGoods, ExchangeTypes, ExchangeCards
from apps.blacklist.models import Maillist, Uidlist
from apps.users.models import Users, GlobalOrders, CallbackOrders
from decimal import Decimal
#from django.shortcuts import get_object_or_404
import logging
from datetime import datetime, timedelta
from django.db.models import Sum

@login_required
def index(request):
    """
        =index  兑换订单
    """

    ft = int(request.GET.get('filter', 0))
    page = int(request.GET.get('page', 1))
    if int(ft) == -1:
        datas = ExchangeOrders.objects.order_by('-create_time')
    else:
        datas = ExchangeOrders.objects.filter(status=ft).order_by('-create_time')
    total = datas.count()
    #ExchangeOrders.objects.filter(id=o['id'],).update(wonder=1)
    cost = datas.aggregate(Sum('total_price'))['total_price__sum']
    if not datas.exists():
        datas = []
    limit = 25
    paginator = Paginator(datas, limit)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    return render_to_response('converts/index.html', {
        'title':      '兑换订单',
        'page_tag':   'converts',
        'username':   request.user.username,
        'datas':      datas,
        'status':     int(ft),
        'total':      total,
        'cost':       cost,
    })

@login_required
def search(request):
    """ 搜索订单 """
    total, query, orders, cost = get_params(request)
    export = request.GET.get('export', 0)
    if export:
        """ 导出订单 """
        response = render_to_response("converts/export_xls.html", {"datas": orders,})
        response['Content-Disposition'] = 'attachment; filename=export_file.xls'
        response['Content-Type'] = 'application/ms-excel; charset=utf-8'
        return response

    # 分页
    status = request.GET.get('status')
    status = int(status) if status else -1
    page = int(request.GET.get('page', 1))
    limit = 200
    paginator = Paginator(orders, limit)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    return render_to_response('converts/search.html', {
        'title': '搜索结果',
        'page_tag': 'converts',
        'username': request.user.username,
        'datas': orders,
        'total': total,
        'query': query,
        'status': status,
        'cost': cost,
    })


@login_required
def codesearch(request):
    """ 搜索兑换码 """
    type_id = request.GET.get('type_id')
    goods_id = request.GET.get('goods_id')
    #ip = request.GET.get('ip')
    num = request.GET.get('num')
    pwd =request.GET.get('pwd')
    flag = True
    total = 0
    params = {}
    if type_id:
        params.setdefault('type_id', type_id)
        flag = False
    if goods_id:
        params.setdefault('goods_id', goods_id)
        flag = False
    #if ip:
    #    params.setdefault('ip', ip)
    #    flag = False
    if num:
        params.setdefault('num', num)
        flag = False

    if pwd:
        params.setdefault('pwd', pwd)
        flag = False

    if not flag:
        codeinfo = ExchangeCards.objects.filter(**params)
        total = codeinfo.count()
    return render_to_response('converts/codesearch.html', {
        'title': '搜索结果',
        'page_tag': 'converts',
        'username': request.user.username,
        'datas': codeinfo,
        'total': total,
    })


def get_params(request):
    """ 获取参数 """
    params = {}
    total = 0
    query = ''
    params_key = ['uid', 'goods_id', 'num', 'pwd', 'status', 'create_time__gte', 'create_time__lte']
    for key in params_key:
        param = request.GET.get(key)
        print `param` +'params'
        query += '%s=%s&' % (key, param)
        print `query` +'query'
        if param:
            params.setdefault(key, param)
    cost = 0
    orders = ExchangeOrders.objects.filter(**params).order_by('-create_time')
    if orders:
        total = orders.count()
        cost = orders.aggregate(Sum('total_price'))['total_price__sum']

    return total, query, orders, cost


@login_required
def acceptConvert(request):
    """
        =accept converts  审核兑换
    """
    def update_status(dotstr, status):
        res = []
        id_list = dotstr.split(',')
        for i in id_list:
            if i:
                order = ExchangeOrders.objects.get(id=i)
                card  = ExchangeCards.objects.filter(goods_id=order.goods_id,status=0).order_by("id")[:1]
                if card :
                    card = card[0]
                    order.num = card.num
                    order.pwd = card.pwd
                    order.end_date = card.end_date
                    order.status = status
                    card.uid = order.uid
                    order.inprice = card.inprice
                    card.status = 1
                    card.save()
                    order.save()
                    res.append({'id':i, 'status':status})
                    blackMail = Maillist.objects.filter(mail=order.address,status=1)
                    if blackMail:
                        res.append({'id':i, 'status':5})
                    blackUid = Uidlist.objects.filter(uid=order.uid, status=1)
                    if blackUid:
                        res.append({'id':i, 'status':5})
                # 现金不需兑换码
                elif (not card) and (order.goods_id==0 or order.goods_id==3 or order.goods_id==6 or \
                                     order.goods_id==13 or order.goods_id==86 or order.goods_id==87 \
                                     or order.goods_id==88):
                    order = ExchangeOrders.objects.get(id=i)
                    order.status = status
                    order.save()
                    res.append({'id':i, 'status':status})
                elif not card:
                    res.append({'id':i, 'status':4})
            return res

    accept = request.POST.get('accept', None)
    wait = request.POST.get('wait', None)
    ignore = request.POST.get('ignore', None)
    delay = request.POST.get('delay', None)

    def update_status1(dotstr, status):
        res = []
        id_list = dotstr.split(',')
        for i in id_list:
            if i:
                order = ExchangeOrders.objects.get(id=i)
                order.status = status
                if (status==2) and (order.duiba==0) and (order.goods_id!=0) :
                    # 非兑吧忽略返回点数
                    Note = '退回點數'
                    count = GlobalOrders.objects.filter(uid=order.uid, type='15').count()
                    if count%4 == 0 and count>0:
                        Note = '當月簽到占任務的80%，因此退回點數'
                    user = Users.objects.get(uid=order.uid)
                    Users.objects.filter(uid=order.uid).update(points=user.points+order.total_points)
                    GlobalOrders.objects.create(uid=order.uid, type='15', note=Note, \
                        last=user.points, points=order.total_points)
                    CallbackOrders.objects.create(order=Note, ad_source='15', platform=3, ad=Note, \
                        user=order.uid, points=order.total_points)
                order.save()
                res.append({'id':i, 'status':status})
        return res

    res = []
    res = update_status(accept, 1)
    res.extend(update_status1(wait, 0))
    res.extend(update_status1(ignore, 2))
    res.extend(update_status1(delay, 3))

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def add_notes(request):
    """ 添加订单备注 """
    res = {}
    res['c'] = -1
    id = request.GET.get('id')
    notes = request.GET.get('notes', '')
    if id:
        order = ExchangeOrders.objects.get(id=id)
        order.notes = notes
        order.save()
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def add_pwd(request):
    """ 添加订单密码 """
    res = {}
    res['c'] = -1
    id = request.GET.get('id')
    pwd = request.GET.get('pwd', '')
    if id:
        order = ExchangeOrders.objects.get(id=id)
        order.pwd = pwd
        order.save()
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def add_num(request):
    """ 添加订单兑换码 """
    res = { 'c':-1 }
    id = request.GET.get('id')
    num = request.GET.get('num', '')
    if id:
        order = ExchangeOrders.objects.get(id=id)
        order.num = num
        order.save()
        res['c'] = 0
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json")

@login_required
def items(request):
    """
        =items  兑换商品管理
    """
    datas = ExchangeGoods.objects.all().order_by('exchange_counts').reverse()

    if not datas.exists():
        datas = []

    return render_to_response('converts/items.html', {
        'title':      '兑换商品',
        'page_tag':   'converts',
        'username':   request.user.username,
        'datas':      datas,
    })


@login_required
def itemAdd(request):
    """
        =item add  添加商品
    """
    errors = []
    succ = False
    posts = {}
    if request.method == 'POST':
        posts = {
            'exchange_type':   int(request.POST.get('exchangeType', 0)),
            'exchange_name':   request.POST.get('exchangeName', ''),
            'exchange_desc':   request.POST.get('exchangeDesc', ''),
            'exchange_cost':   float(request.POST.get('exchangeCost', 1)),
            'exchange_point':  int(request.POST.get('exchangePoint',1))
        }

        # 检查表单值
        if not posts['exchange_name']:
            errors.append('请输入一个商品名字')
        if not posts['exchange_desc']:
            errors.append('请添加商品描述')
        if not posts['exchange_cost']:
            errors.append('请填写正确商品价格')

        # 计算消耗钻石
        #posts['exchange_point'] = int(posts['exchange_cost'] * 1000)

        if not errors:
            ExchangeGoods.objects.create(type_id=posts['exchange_type'],
                title=posts['exchange_name'], description=posts['exchange_desc'],
                price=posts['exchange_cost'], points=posts['exchange_point'])

            succ = True
            posts = {}  #清空

    datas = ExchangeTypes.objects.all()
    if not datas.exists():
        datas = []

    return render_to_response('converts/item_add.html', {
        'title':       '添加兑换商品',
        'page_tag':    'converts',
        'username':    request.user.username,
        'datas':       datas,
        'errors':      errors,
        'succ':        succ,
        'temps':       posts,
    })


@login_required
def itemEdit(request):
    """
        =item edit  编辑商品
    """
    errors = []
    succ = False
    posts = {}
    checked = 0
    gid = 0
    if request.method == 'POST':
        posts = {
            'exchange_gid':    int(request.POST.get('exchangeGid', 0)),
            'exchange_type':   int(request.POST.get('exchangeType', 0)),
            'exchange_name':   request.POST.get('exchangeName', ''),
            'exchange_desc':   request.POST.get('exchangeDesc', ''),
            'exchange_cost':   float(request.POST.get('exchangeCost', 1)),
            'exchange_point':  int(request.POST.get('exchangePoint',1)),
            'status':   int(request.POST.get('status', 1)),
        }
        gid = posts['exchange_gid']
        checked = posts['exchange_type']

        # 检查表单值
        if not posts['exchange_name']:
            errors.append('请输入一个商品名字')
        if not posts['exchange_desc']:
            errors.append('请添加商品描述')
        if not posts['exchange_cost']:
            errors.append('请填写正确商品价格')
        if not posts['exchange_point']:
            errors.append('请填写正确商品积分')

        if not errors:
            ExchangeGoods.objects.filter(goods_id=gid).update(type_id=posts['exchange_type'],
                title=posts['exchange_name'], description=posts['exchange_desc'],
                price=posts['exchange_cost'], status=posts['status'], points=posts['exchange_point'])

            succ = True

    elif request.method == 'GET':
        gid = request.GET.get('gid', 0)
        res = ExchangeGoods.objects.get(goods_id=gid)
        posts = {
            'exchange_type':   res.type_id,
            'exchange_name':   res.title,
            'exchange_desc':   res.description,
            'exchange_cost':   res.price,
            'exchange_point':  res.points,
            'status':  res.status,
        }
        checked = res.type_id
    else:
        return None

    datas = ExchangeTypes.objects.all()
    if not datas.exists():
        datas = []

    return render_to_response('converts/item_edit.html', {
        'title':       '添加兑换商品',
        'page_tag':    'converts',
        'username':    request.user.username,
        'gid':         gid,
        'datas':       datas,
        'checked':     checked,
        'errors':      errors,
        'succ':        succ,
        'temps':       posts
    })


@login_required
def itemDelete(request):
    """
        =delete goods  删除商品
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认删除
    if gid:
        ExchangeGoods.objects.get(goods_id=gid).delete()
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")


@login_required
def types(request):
    """
        =item add type  添加商品类型
    """
    if request.method == 'POST':
        return typeAdd(request)
    else:
        datas = ExchangeTypes.objects.all()

        if not datas.exists():
            datas = []

    return render_to_response('converts/types.html', {
        'title':       '添加商品类型',
        'page_tag':    'converts',
        'username':    request.user.username,
        'datas':       datas,
        })


@login_required
def typeAdd(request):
    """
        = add type 添加兑换类型
    """
    import os
    import Image
    from config.settings import IMG_DIR, BASE_DIR


    posts = {}
    errors = []
    succ = False

    sw = 72
    sh = 72

    if request.method == 'POST':
        #获取前台传过来的新增商品类型信息
        file_obj = request.FILES.get('exchangeTypeIcon', None)
        posts = {
                'exchangeTypeName' : request.POST.get('exchangeTypeName', ''),
                'exchangeTypeAddr' : request.POST.get('exchangeTypeAddr', ''),
                'exchangeTid' : int(request.POST.get('exchangeTid',1)),
                'priority' : int(request.POST.get('priority', 0))
        }
        if not file_obj:
            errors.append("请输入类型图标")
        else:
            image = Image.open(file_obj)
            (width, height) = image.size
            if width > sw or height > sh:
                errors.append("图标规格不正确，请选择至多72*72的图标上传")
        if not posts['exchangeTypeName']:
            errors.append("请输入类型名称")
        if not posts['priority']:
            errors.append("请输入优先级")

        if not errors:
            file_name = getTimeStamp()+".png"
            name = IMG_DIR
            file_dir = os.path.join(BASE_DIR, name)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_dir = file_dir + file_name

            posts['exchangeTypeIcon'] = 'goods/' + file_name
            ExchangeTypes.objects.create(title=posts['exchangeTypeName'],tid=posts['exchangeTid'], icon=posts['exchangeTypeIcon'],priority=posts['priority'], address_type=posts['exchangeTypeAddr'])
            with open(file_dir, 'wb') as dest:
                for chunk in file_obj.chunks():
                    dest.write(chunk)
            succ = True


    datas = ExchangeTypes.objects.all()
    if not datas:
        datas = []

    return render_to_response('converts/types.html', {
            'title' : '添加兑换类型',
            'page_tag' : 'converts',
            'username' : request.user.username,
            'errors' : errors,
            'succ' : succ,
            'datas' : datas,
        })


@login_required
def typeEdit(request):
    """
        = edit type 编辑选中兑换类型
    """

    posts = {}
    errors = []
    succ = False

    if request.method == 'POST':
        #保存信息
        posts = {
                'exchangeTypeId' : request.POST.get('id', 0),
                'exchangeTypeName' : request.POST.get('exchangeTypeName', ''),
                'exchangeTypeAddr' : request.POST.get('exchangeTypeAddr', ''),
                #'exchangeTid' : int(request.POST.get('exchangeTid','')),
                'priority' :int(request.POST.get('priority', 0)),
                'channel' :int(request.POST.get('channel', 0))
            }
        #检查表单有效性
        if not posts['exchangeTypeId']:
            errors.append("修改失败，请重试修改")
        if not posts['exchangeTypeName']:
            errors.append("请输入类型名称")
        if not errors:
            ExchangeTypes.objects.filter(id=posts['exchangeTypeId']).update(title=posts['exchangeTypeName'], \
                priority=posts['priority'], address_type=posts['exchangeTypeAddr'], channel=posts['channel'])
            succ = True
        res = ExchangeTypes.objects.get(id=posts['exchangeTypeId'])
        posts = {
                'id' : res.id,
                'exchangeTypeName' : res.title,
                'exchangeTypeIcon' : res.icon,
                'exchangeTypeAddr' : res.address_type,
                'priority' : res.priority,
                'channel' : res.channel
           }

    elif request.method == 'GET':
        #查询当前类型信息
        tid = request.GET.get('tid', 0)
        res = ExchangeTypes.objects.get(id=tid)
        posts = {
                'id' : res.id,
                'exchangeTypeName' : res.title,
                'exchangeTypeIcon' : res.icon,
                'exchangeTypeAddr' : res.address_type,
                'priority' : res.priority,
                'channel' : res.channel
           }

    return render_to_response('converts/type_edit.html', {
            'title' : '编辑兑换类型',
            'errors' : errors,
            'succ' : succ,
            'temps' : posts,
        })

@login_required
def typeDelete(request):
    """
        = delete type 删除选中兑换类型
    """
    from config.settings import BASE_DIR
    res = {'c' : -1}
    tid = request.GET.get('tid', None)

    if tid:
        e = ExchangeTypes.objects.get(id=tid)
        oldAddr = e.icon
        e.delete()
        delFile(BASE_DIR + oldAddr)
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")


def saveImg(img, file_dir):
    """
        = 保存图片到指定路径
    """
    with open(file_dir, 'wb') as dest:
        for chunk in img.chunks():
            dest.write(chunk)

def delFile(file_dir):
    import os
    try:
        os.remove(file_dir)
    except:
        return None

def getTimeStamp():
    import time
    import random
    return str(time.strftime('%Y-%m-%d-%H-%M-%S')) + '_' + str(random.randint(1, 10000))

@login_required
def codes(request):
    """
    =code add  兑换码录入
    """
    errors = []
    succ = False
    posts = {}
    if request.method == 'POST':
        posts = {
            'exchange_good':   int(request.POST.get('exchangeGood', 1)),
            'exchange_title':  ExchangeGoods.objects.filter(goods_id=int(request.POST.get('exchangeGood', 1))).values('title')[0]['title'],
            'exchange_type':  ExchangeGoods.objects.filter(goods_id=int(request.POST.get('exchangeGood', 1))).values('type_id')[0]['type_id'],
            'NumPwd':           request.POST.get('NumPwd', ''),
            #'exchange_num':    request.POST.get('exchangeNum', ''),
            #'exchange_pwd':    request.POST.get('exchangePwd', ''),
            'exchange_inprice':    Decimal(request.POST.get('exchangeInprice', '')),
            'end_date':    request.POST.get('end_date', ''),
            'exchange_outprice':    ExchangeGoods.objects.filter(goods_id=int(request.POST.get('exchangeGood', 1))).values('price')[0]['price'],
        }
        # 检查表单值
        if not posts['exchange_good']:
            errors.append('请选择兑换卡名')
        if not posts['exchange_inprice']:
            errors.append('请输入进货价')
        if not posts['end_date']:
            errors.append('有效期')
        if not errors:
            strNumPwd = ":".join(request.POST.get('NumPwd', ''))
            #NP = strNumPwd.replace(":","").replace(" ","").split(";")
            NP = strNumPwd.replace(":","").split("\r\n")
            logging.info(NP)
            for np in NP:
                StrNp = np.lstrip().split(" ")
                tempnum = StrNp[0]
                StrNp = np.rstrip().split(" ")
                for i in StrNp:
                    i.strip()
                    if i.startswith(" ")!=True:
                        temppwd= i
                    if tempnum == temppwd:
                        temppwd=''
                if posts['exchange_type'] != 29 and posts['exchange_type'] !=30 :
                    ExchangeCards.objects.create( goods_id=posts['exchange_good'], title=posts['exchange_title'], \
                        type_id=posts['exchange_type'], num=tempnum, pwd=temppwd, \
                        inprice=posts['exchange_inprice'], outprice=posts['exchange_outprice'], status=0, end_date=posts['end_date'])
                else:
                    ExchangeCards.objects.create( goods_id=posts['exchange_good'], title=posts['exchange_title'], \
                        type_id=posts['exchange_type'], num=tempnum,  \
                        inprice=posts['exchange_inprice'], outprice=posts['exchange_outprice'], status=0, end_date=posts['end_date'])
            succ = True
            posts = {}  #清空

    datas = ExchangeGoods.objects.all()
    if not datas.exists():
        datas = []

    return render_to_response('converts/codes.html', {
        'title':       '兑换码录入',
        'page_tag':    'converts',
        'username':    request.user.username,
        'datas':       datas,
        'errors':      errors,
        'succ':        succ,
        'temps':       posts,
        })



@login_required
def codeinfo(request):
    """ 兑换码信息概况 """
    limit = 25
    orderbygd = orderby = request.GET.get('orderby', 'goods_id')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))

    if not updw:
        orderbyud = '-' + orderby
    datas = ExchangeCards.objects.order_by(orderbygd)
    #titles = ExchangeGoods.objects.get(goods_id=3)
    if not datas.exists():
        datas = []

    paginator = Paginator(datas, limit)

    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    return render_to_response('converts/codeinfo.html', {
        'title':    '兑换码信息',
        'page_tag': 'converts',
        'username': request.user.username,
        'datas':    datas,
	#'titles':   titles,
        'orderby':  orderby,
        'updw':     updw,
    })


@login_required
def codeEdit(request):
    """
        =code edit  编辑兑换码
    """
    errors = []
    succ = False
    posts = {}
    checked = 0
    gid = 0
    if request.method == 'POST':
        posts = {
            'exchange_gid':    int(request.POST.get('exchangeGid', 0)),
            #'exchange_gid':    int(request.POST.get('gid', 0)),
            'exchange_good':   int(request.POST.get('exchangeGood', 1)),
	    'exchange_title':  ExchangeGoods.objects.filter(goods_id=int(request.POST.get('exchangeGood', 1))).values('title')[0]['title'],
	    'exchange_type':  ExchangeGoods.objects.filter(goods_id=int(request.POST.get('exchangeGood', 1))).values('type_id')[0]['type_id'],
            'exchange_num':    request.POST.get('exchangeNum', ''),
            'exchange_pwd':    request.POST.get('exchangePwd', ''),
            'exchange_inprice':    request.POST.get('exchangeInprice', 0),
            'exchange_outprice':    request.POST.get('exchangeOutprice', 0),
            'exchange_status':   int(request.POST.get('exchangeStatus', 0)),
        }
        gid = posts['exchange_gid']
        checked = posts['exchange_type']

        # 检查表单值
        if not posts['exchange_good']:
            errors.append('请选择兑换卡名')
        if not posts['exchange_num']:
            errors.append('请输入兑换码')
        if not posts['exchange_pwd']:
            errors.append('请输入密码')
        if not posts['exchange_inprice']:
            errors.append('请输入进货价')
        if not posts['exchange_outprice']:
            errors.append('请输入售出价')

        if not errors:
            ExchangeCards.objects.filter(id=gid).update(goods_id=posts['exchange_good'], title=posts['exchange_title'],
                type_id=posts['exchange_type'], num=posts['exchange_num'], pwd=posts['exchange_pwd'],
		    inprice=posts['exchange_inprice'], outprice=posts['exchange_outprice'],
		    status=posts['exchange_status'])

            succ = True

    elif request.method == 'GET':
        gid = request.GET.get('gid', 0)
        res = ExchangeCards.objects.get(id=gid)
        posts = {
            'exchange_good':   res.goods_id,
            'exchange_num':   res.num,
            'exchange_pwd':   res.pwd,
            'exchange_inprice':   res.inprice,
            'exchange_outprice':   res.outprice,
            'exchange_status':  res.status
        }
        checked = res.type_id
    else:
        return None

    datas = ExchangeGoods.objects.all()
    if not datas.exists():
        datas = []

    return render_to_response('converts/codeinfo_edit.html', {
        'title':       '编辑兑换商品',
        'page_tag':    'converts',
        'username':    request.user.username,
        'gid':         gid,
        'datas':       datas,
        'checked':     checked,
        'errors':      errors,
        'succ':        succ,
        'temps':       posts
    })


@login_required
def codeStatus(request):
    """
        =code status  更改兑换码状态
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认更改
    if gid:
        ExchangeCards.objects.filter(id=gid).update(status=posts['exchange_status'])
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")


@login_required
def codeinfoDelete(request):
    """
        =delete codeinfo  删除兑换码
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认删除
    if gid:
        ExchangeCards.objects.get(id=gid).delete()
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")


@login_required
def codedetailDelete(request):
    """
        =兑换卡明细删除兑换码
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认删除
    if gid:
        ExchangeCards.objects.get(id=gid).delete()
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def codedetail(request, gid=0):
    """ 兑换卡信息 """
    gid = int(gid)
    cur_card = {}
    cur_card['gid'] = gid

    # 兑换卡信息
    goodcards = ExchangeGoods.objects.exclude(type_id=24).order_by('-exchange_counts')
    for c in goodcards:
        if c.goods_id == gid:
            logging.debug(c.goods_id)
            cur_card['title'] = c.title
    if not gid:
        cur_card['title'] = '全部'

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

    if gid:
        cards = ExchangeCards.objects.filter(
            goods_id=gid, time__gte=date_start, time__lt=date_end).order_by('-status').reverse()
        #未使用卡
        newcards = ExchangeCards.objects.filter(
            goods_id=gid, status=0, time__gte=date_start, time__lt=date_end).order_by('-time')
    else:
        cards = ExchangeCards.objects.filter(
            time__gte=date_start, time__lt=date_end).order_by('-status').reverse()
        newcards = ExchangeCards.objects.filter(
            status=0, time__gte=date_start, time__lt=date_end).order_by('-time')


    # 总下载数，总积分
    summary = dict(
        count=cards.count(),
        newcount=newcards.count(),
        inprice=cards.aggregate(Sum('inprice'))['inprice__sum'],
    )
    # 分页
    limit = 25
    paginator = Paginator(cards, limit)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)

    return render_to_response('converts/codedetail.html', {
        'title':    '兑换卡信息',
        'page_tag': 'converts',
        'username': request.user.username,
        'datas': cards,
        'card': goodcards,
        'cur_card': cur_card,
        'query_date': date_start,
        'query_enddate': date_end,
        'summary': summary,
    })

@login_required
def codedetailUsed(request):
    """
        =兑换卡已使用
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认
    if gid:
        card = ExchangeCards.objects.get(id=gid)
        card.status=1
        card.save()
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def codedetailUnused(request):
    """
        =兑换卡未使用
    """
    res = { 'c': -1 }

    gid = request.GET.get('gid', None)

    # 确认
    if gid:
        card = ExchangeCards.objects.get(id=gid)
        card.status=0
        card.save()
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required
def codedetail_edit(request):
    """ 发放奖励 """
    errors = []
    succ = False
    if request.method == 'GET':
        id = request.GET.get('id', 0)
        if id:
            datas = ExchangeCards.objects.get(id=id)
        else:
            return None
    elif request.method == 'POST':
        datas = {
            'id':          int(request.POST.get('id', 0)),
            'uid':           int(request.POST.get('uid', 0)),
            'goods_id':     int(request.POST.get('goods_id', 0)),
            'type_id':      int(request.POST.get('type_id', 0)),
            'inprice':        request.POST.get('inprice', 0),
            'outprice':        request.POST.get('outprice', 0),
            'title':         request.POST.get('title', ''),
            'num':          request.POST.get('num', ''),
            'pwd':          request.POST.get('pwd', ''),
            'notes':       request.POST.get('notes', ''),
            'appType':       int(request.POST.get('appType', 0)),
        }
        if datas['id']:
            if not datas['notes']:
                errors.append('请输入备注')
            elif not datas['uid']:
                errors.append('请输入用户id')
        else:
            return None
        if not errors:
            good = ExchangeGoods.objects.get(goods_id = datas['goods_id'])
            ExchangeOrders.objects.create(uid=datas['uid'], points = good.points, oid=0, \
                    inprice = datas['inprice'],price = datas['outprice'], \
                    total_price = datas['outprice'], total_points = good.points, \
                    goods_id = datas['goods_id'], goods_title = datas['title'], \
                    count = 1, status = 1, duiba = 0, num = datas['num'], pwd = datas['pwd'], \
                    notes = datas['notes'], type_id = datas['type_id'], appType=datas['appType'])
            ExchangeCards.objects.filter(id=datas['id']).update(status=1, uid = datas['uid'], changetime = datetime.now())
            '''
            CallbackOrders.objects.create(order=datas['note'], ad_source='10', platform=3, ad="GooglePlay五星好評", \
                user=datas['uid'], points=int(datas['addpoints']))
            Users.objects.filter(uid=datas['uid']).update(points=(int(datas['points'])+int(datas['addpoints'])))
            GlobalOrders.objects.create(uid=datas['uid'], type='9', note=datas['note'], \
                last=datas['points'], points=int(datas['addpoints']))
            CallbackOrders.objects.create(order=datas['note'], ad_source='9', platform=3, ad=datas['note'], \
                ser=datas['uid'], points=int(datas['addpoints']))
            '''
        succ = True
    else:
        return None
    return render_to_response('converts/codedetail_edit.html', {
        'title': '发放奖励',
        'page_tag': 'converts',
        'datas': datas,
        'succ': succ,
        'errors': errors,
    })



