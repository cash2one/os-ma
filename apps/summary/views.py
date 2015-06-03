#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author chenjiehua@youmi.net,lisongjian@youmi.net
#

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from apps.summary.models import Callback, Income
from apps.users.models import Users
from datetime import date, timedelta, datetime
from django.db.models import Sum, Count
import operator, json
from apps.converts.models import ExchangeOrders
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal

@login_required
def index(request):
    """ 汇总数据 """

    today = date.today()

    # 用户情况
    total_user = Users.objects.count()
    new_user = Users.objects.filter(
        create_at__gte=(today)).count()
    #new_user_fromad = Users.objects.filter.count()
    new_user_ios = Users.objects.filter(
        create_at__gte=(today),platform=2).count()

    # 今日积分情况
    today_total_points = Callback.objects.filter(
        time__gte=(today)).aggregate(Sum('points'))['points__sum'],
    today_total_points = today_total_points[0] if today_total_points[0] else 0

    today_callback_orders = Callback.objects.filter(
        time__gte=(today)).count()
    today_callback_orders = today_callback_orders if today_callback_orders else 0

    per_order_points = (today_total_points / today_callback_orders) \
        if today_callback_orders > 0 else 0

    # 用户状态
    seven_days_ago = today - timedelta(days=7)
    new_user_stats = Users.objects \
        .filter(create_at__gte=seven_days_ago, platform='1', appType=0) \
        .extra({'date_create_at': "DATE(create_at)"}) \
        .values('date_create_at') \
        .annotate(dcount=Count('uid'))
    new_user_ios_stats = Users.objects \
        .filter(create_at__gte=seven_days_ago, platform='2', appType=0) \
        .extra({'date_create_at': "DATE(create_at)"}) \
        .values('date_create_at') \
        .annotate(dcount=Count('uid'))
    new_user_kaka_stats = Users.objects \
        .filter(create_at__gte=seven_days_ago, platform='1', appType=1) \
        .extra({'date_create_at': "DATE(create_at)"}) \
        .values('date_create_at') \
        .annotate(dcount=Count('uid'))

    user_stats = {}
    for stat in new_user_stats:
        user_stats[stat['date_create_at']] = {
            'aos': stat['dcount'] if stat['dcount'] else 0,
            'ios': 0,
            'kaka': 0
        }
    for stat in new_user_ios_stats:
        user_stats[stat['date_create_at']]['ios'] = stat['dcount'] if stat['dcount'] else 0
    for stat in new_user_kaka_stats:
        user_stats[stat['date_create_at']]['kaka'] = stat['dcount'] if stat['dcount'] else 0

    aos_callback_stats = Callback.objects \
        .filter(time__gte=seven_days_ago, platform=3, appType=0) \
        .extra({'date_create_at': "DATE(time)"}) \
        .values('date_create_at')
    ios_callback_stats = Callback.objects \
        .filter(time__gte=seven_days_ago, platform=5, appType=0) \
        .extra({'date_create_at': "DATE(time)"}) \
        .values('date_create_at')
    kaka_callback_stats = Callback.objects \
        .filter(time__gte=seven_days_ago, platform=3, appType=1) \
        .extra({'date_create_at': "DATE(time)"}) \
        .values('date_create_at')

    points_stats = {}
    #fixme 当有ios积分/用户没有aos会报错
    for stat in aos_callback_stats.annotate(dcount=Sum('points')):
        for d in stat:
            points_stats[stat['date_create_at']] = {
            'aos': stat['dcount'] if stat['dcount'] else 0,
            'ios': 0,
            'kaka': 0
            }
    for stat in ios_callback_stats.annotate(dcount=Sum('points')):
        for d in stat:
            points_stats[stat['date_create_at']]['ios'] = stat['dcount'] if stat['dcount'] else 0
    for stat in kaka_callback_stats.annotate(dcount=Sum('points')):
        for d in stat:
            points_stats[stat['date_create_at']]['kaka'] = stat['dcount'] if stat['dcount'] else 0


    tasks_stats = {}
    for stat in aos_callback_stats.annotate(dcount=Count('id')):
        for d in stat:
            tasks_stats[stat['date_create_at']] = {
            'aos': stat['dcount'] if stat['dcount'] else 0,
            'ios': 0,
            'kaka': 0
           }
    for stat in ios_callback_stats.annotate(dcount=Count('id')):
        for d in stat:
            tasks_stats[stat['date_create_at']]['ios'] = stat['dcount'] if stat['dcount'] else 0
    for stat in kaka_callback_stats.annotate(dcount=Count('id')):
        for d in stat:
            tasks_stats[stat['date_create_at']]['kaka'] = stat['dcount'] if stat['dcount'] else 0


    return render_to_response('summary/index.html', {
        'title':    '汇总数据',
        'page_tag': 'summary',
        'total_user': total_user,
        'today_total_points': today_total_points,
        'today_callback_orders': today_callback_orders,
        'new_user': new_user,
       # 'new_user_fromad': new_user_fromad,
        'per_order_points': per_order_points,
        'user_stats': user_stats,
        'points_stats': points_stats,
        'tasks_stats': tasks_stats,
    })

def get_querydate(request):
    date_se = {}
    query_date = {}
    query_date['s'] = request.GET.get('s', '')
    query_date['e'] = request.GET.get('e', '')

    if not query_date['e']:
        query_date['e'] = date.today() + timedelta(days=1)
        date_se['e'] = date.today().strftime("%Y-%m-%d")
        if not query_date['s']:
            query_date['s'] = date.today() - timedelta(days=14)
            date_se['s'] = query_date['s'].strftime("%Y-%m-%d")
        else:
            date_se['s'] = query_date['s']
    else:
        date_se['e'] = query_date['e']
        query_datetime = datetime.strptime(query_date['e'], "%Y-%m-%d").date()
        query_date['e'] = query_datetime + timedelta(days=1)
        if not query_date['s']:
            query_date['s'] = query_datetime - timedelta(days=14)
            date_se['s'] = query_date['s'].strftime("%Y-%m-%d")
        else:
            date_se['s'] = query_date['s']

    return (query_date, date_se)

@login_required
def earns(request):
    """ 赚取统计 """

    query_date, date_se = get_querydate(request)
    date = request.GET.get('date')
    enddate = request.GET.get('enddate')
    if not date:
        date_start = datetime.strftime(datetime.now(), "%Y-%m-01")
        date_end = datetime.strftime(datetime.now()+timedelta(days=1), "%Y-%m-%d")
    else:
        date_start = date
        date_end = enddate
    earns_stats = Callback.objects \
        .filter(time__gte=date_start, time__lte=date_end) \
        .extra({'order_time': "DATE(time)"}) \
        .values('order_time', 'ad_source') \
        .annotate(dcount=Count('id'), dsum=Sum('points'))

    ad = ['total', 'youmi', 'supersonic', 'aarki', 'fyber', 'newuser', 'share', 'invite', 'sign', 'like', 'star', 'earnPoint']
    ad_id = [-1, 107,104,103, 108, 1, 2, 3, 4, 8, 11, 17]
    tmp = {}

    for e in earns_stats:
        # 每天数据统计
        tmp.setdefault(e['order_time'], {}.fromkeys(ad))
        if not tmp[e['order_time']]['total']:
            tmp[e['order_time']]['total'] = {
                'down': e['dcount'],
                'earns': e['dsum'],
            }
        else:
            tmp[e['order_time']]['total']['down'] += e['dcount']
            tmp[e['order_time']]['total']['earns'] += e['dsum']

        if e['ad_source'] in ad_id:
            # 每天数据统计
            tmp[e['order_time']][ad[ad_id.index(e['ad_source'])]] = {
                'down': e['dcount'],
                'earns': e['dsum'],
            }

    datas = []
    total = {}.fromkeys(ad)
    for t in tmp:
        for a in tmp[t]:
            if not tmp[t][a]:
                tmp[t][a] = dict(down=0, earns=0)
        # 累积数据
        for k in total:
            if not total[k]:
                total[k] = {
                    'down': tmp[t][k]['down'],
                    'earns': tmp[t][k]['earns'],
                }
            else:
                total[k]['down'] += tmp[t][k]['down']
                total[k]['earns'] += tmp[t][k]['earns']

        tmp[t].setdefault('time', t)
        datas.append(tmp[t])
    datas = sorted(datas, key=operator.itemgetter('time'), reverse=True)

    return render_to_response('summary/earns.html', {
        'title': '赚取统计',
        'page_tag': 'earns',
        'datas': datas,
        'date_se': date_se,
        'total': total,
    })

@login_required
def income(request):
    """ 财务统计 """
    limit = 100
    #orderbyud = orderby = request.GET.get('orderby', 'id')
    updw = int(request.GET.get('updw', 0))
    page = int(request.GET.get('page', 1))
    dates = request.GET.get('date')
    enddate = request.GET.get('enddate')
    if not dates:
        date_start = datetime.strftime(datetime.now(), "%Y-%m-01")
        date_end = datetime.strftime(datetime.now()+timedelta(days=1), "%Y-%m-%d")
    else:
        date_start = dates
        date_end = enddate
    # if not updw:
    #    orderbyud = '-' + orderby
    datas= Income.objects.filter(
            day__gte=date_start, day__lt=date_end).order_by('-id')
         # 累积数据
    if not datas.exists():
        datas = []
    youmi=vungle=supersonic=aarki=woobi=duiba_cost=self_cost= \
        adcolony=trialpay=fyber=metaps=appdriver=adxmi= \
        admob=duomeng=dincome=rincome=cost=paypal_cost=airpush= \
        personaly=0
    for d in datas:
        youmi += d.youmi
        adxmi += d.adxmi
        vungle += d.vungle
        supersonic +=d.supersonic
        aarki += d.aarki
        adcolony += d.adcolony
        trialpay +=d.trialpay
        fyber +=d.fyber
        metaps +=d.metaps
        appdriver +=d.appdriver
        admob +=d.admob
        duomeng +=d.duomeng
        woobi +=d.woobi
        airpush +=d.airpush
        personaly +=d.personaly
        dincome +=d.dincome
        rincome +=d.rincome
        duiba_cost +=d.duiba_cost
        paypal_cost +=d.paypal_cost
        self_cost +=d.self_cost
        cost +=d.cost

    total = {
            'youmi':       youmi,
            'adxmi':       adxmi,
            'vungle':      vungle,
            'supersonic':  supersonic,
            'aarki':       aarki,
            'adcolony':   adcolony,
            'trialpay':    trialpay,
            'fyber':       fyber,
            'metaps':       metaps,
            'appdriver':    appdriver,
            'admob':       admob,
            'duomeng':     duomeng,
            'woobi':      woobi,
            'airpush':      airpush,
            'personaly':    personaly,
            'dincome':       dincome,
            'rincome':     rincome,
            'duiba_cost': duiba_cost,
            'self_cost':  self_cost,
            'paypal_cost':  paypal_cost,
            'cost':       cost,
            'gprofit':      rincome-cost,
            'gmargin':      ("%.2f" % ((rincome-cost)/cost*100)),
            }
    if not datas.exists():
        datas = []

    paginator = Paginator(datas, limit)

    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    return render_to_response('summary/income.html', {
        'title':    '财务统计',
        'page_tag': 'summary',
        'username': request.user.username,
        'datas':    datas,
        'updw':     updw,
        'total':    total,
    })

@login_required
def income_edit(request):
    """ 收入编辑 """
    errors = []
    succ = False
    if request.method == 'GET':
        id = request.GET.get('id', 0)
        if id:
            datas = Income.objects.get(id=id)
        else:
            return None
    elif request.method == 'POST':
        datas = {
            'id':           int(request.POST.get('id', 0)),
            'day':       request.POST.get('day', ''),
            'dollar':       Decimal(request.POST.get('dollar', 0)),
            'youmi':       Decimal(request.POST.get('youmi', 0)),
            'adxmi':       Decimal(request.POST.get('adxmi', 0)),
            'vungle':       Decimal(request.POST.get('vungle', 0)),
            'supersonic':       Decimal(request.POST.get('supersonic', 0)),
            'aarki':       Decimal(request.POST.get('aarki', 0)),
            'adcolony':       Decimal(request.POST.get('adcolony', 0)),
            'trialpay':       Decimal(request.POST.get('trialpay', 0)),
            'fyber':       Decimal(request.POST.get('fyber', 0)),
            'metaps':       Decimal(request.POST.get('metaps', 0)),
            'appdriver':       Decimal(request.POST.get('appdriver', 0)),
            'admob':       Decimal(request.POST.get('admob', 0)),
            'duomeng':       Decimal(request.POST.get('duomeng', 0)),
            'woobi':       Decimal(request.POST.get('woobi', 0)),
            'airpush':       Decimal(request.POST.get('airpush', 0)),
            'personaly':       Decimal(request.POST.get('personaly', 0)),
            'dincome':       Decimal(request.POST.get('dincome', 0)),
            'rincome':       Decimal(request.POST.get('rincome', 0)),
            'cost':       Decimal(request.POST.get('cost', 0)),
            'gprofit':       Decimal(request.POST.get('gprofit', 0)),
            'gmargin':       Decimal(request.POST.get('gmargin', 0)),
            }
        if not errors:
            Income.objects.filter(id=datas['id']).update(youmi=datas['youmi'], adxmi=datas['adxmi'], vungle=datas['vungle'], \
                    supersonic=datas['supersonic'], aarki=datas['aarki'], adcolony=datas['adcolony'], \
                    trialpay=datas['trialpay'], fyber=datas['fyber'], metaps=datas['metaps'], \
                    appdriver=datas['appdriver'], admob=datas['admob'], duomeng=datas['duomeng'], \
                    dincome=datas['dincome'], rincome=datas['rincome'], cost=datas['cost'], woobi=datas['woobi'], \
                    gprofit=datas['gprofit'], gmargin=datas['gmargin'], dollar=datas['dollar'], airpush=datas['airpush'], personaly=datas['personaly'])
        succ = True

    return render_to_response('summary/income_edit.html', {
        'title': '收入修改',
        'page_tag': 'summary',
        'username': request.user.username,
        'datas': datas,
        'succ': succ,
        'errors': errors,
    })

@login_required
def income_count(request):
    """
        计算成本
    """
    res = { 'c': -1 }

    id = request.GET.get('id', None)

    # 确认删除
    if id:
        income = Income.objects.get(id=id)
        dincome = income.youmi+income.adxmi+income.vungle+income.supersonic+income.aarki+income.adcolony+ \
            income.trialpay+income.fyber+income.metaps+income.appdriver+income.admob+ \
            income.duomeng+income.woobi+income.airpush + income.personaly
        print dincome
        print 'dincome'
        rincome = dincome*income.dollar
        total_inprice = ExchangeOrders.objects.filter(
            create_time__gte=(income.day),create_time__lte=(income.day+timedelta(days=1)), status=1, duiba=0).aggregate(Sum('inprice'))['inprice__sum'],
        total_inprice = total_inprice[0] if total_inprice[0] else 0
        duiba_inprice = ExchangeOrders.objects.filter(
            create_time__gte=(income.day),create_time__lte=(income.day+timedelta(days=1)), status=1, duiba=1).aggregate(Sum('total_price'))['total_price__sum'],
        duiba_inprice = duiba_inprice[0] if duiba_inprice[0] else 0
        paypal_inprice1 = ExchangeOrders.objects.filter(
            create_time__gte=(income.day),create_time__lte=(income.day+timedelta(days=1)), status=1, goods_id=86).aggregate(Sum('total_price'))['total_price__sum'],
        paypal_inprice1 = paypal_inprice1[0] if paypal_inprice1[0] else 0
        paypal_inprice3 = ExchangeOrders.objects.filter(
            create_time__gte=(income.day),create_time__lte=(income.day+timedelta(days=1)), status=1, goods_id=88).aggregate(Sum('total_price'))['total_price__sum'],
        paypal_inprice3 = paypal_inprice3[0] if paypal_inprice3[0] else 0
        paypal_inprice5 = ExchangeOrders.objects.filter(
            create_time__gte=(income.day),create_time__lte=(income.day+timedelta(days=1)), status=1, goods_id=87).aggregate(Sum('total_price'))['total_price__sum'],
        paypal_inprice5 = paypal_inprice5[0] if paypal_inprice5[0] else 0
        total_price = total_inprice + duiba_inprice + paypal_inprice1 + paypal_inprice3 +paypal_inprice5
        gprofit = rincome-total_price
        if total_price>0:
            gmargin = (gprofit/total_price)*100
            gmargin = ("%.2f" % gmargin)
            income.dincome=dincome
            income.rincome=rincome
            income.duiba_cost = duiba_inprice
            income.self_cost = total_inprice
            income.cost = total_price
            income.gprofit = gprofit
            income.gmargin = gmargin
            income.paypal_cost = paypal_inprice1 + paypal_inprice3 + paypal_inprice5
            income.save()
        else:
            income.dincome = dincome
            income.rincome = rincome
            income.save()
        res['c'] = 0

    return HttpResponse(json.dumps(res), content_type="application/json")

