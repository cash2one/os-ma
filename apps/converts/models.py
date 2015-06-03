#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author chenjiehua@youmi.net,lisongjian@youmi.net
#

from django.db import models
from apps.users.models import Users


# 兑换订单
class ExchangeOrders(models.Model):
    class Meta:
        db_table = 'exchange_orders'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'%s Order ID:%d' % (self.goods_title, self.oid)

    id = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    oid = models.IntegerField()
    points = models.IntegerField()
    total_points = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=3)
    goods_id = models.IntegerField()
    goods_title = models.CharField(max_length=128)
    count = models.SmallIntegerField()
    status = models.SmallIntegerField()
    duiba = models.SmallIntegerField()
    num = models.CharField(max_length=30)
    notes = models.TextField()
    pwd = models.TextField()
    address = models.TextField()
    create_time = models.DateTimeField()
    appType = models.IntegerField()
    wonder = models.IntegerField()
    inprice = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    type_id = models.IntegerField()
    end_date = models.DateTimeField()

    @property
    def users(self):
        return Users.objects.get(uid=self.uid)

    @property
    def points_format(self):
        return '{:,.0f}'.format(self.points)


# 兑换种类
class ExchangeTypes(models.Model):
    class Meta:
        db_table = 'exchange_types'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'%s Type ID:%d' % (self.title, self.id)

    id = models.AutoField(primary_key=True)
    title = models.CharField(128)
    icon = models.CharField(512)
    address_type = models.CharField(32)
    priority = models.IntegerField(3)
    tid = models.IntegerField()
    channel = models.IntegerField()


# 兑换项目
class ExchangeGoods(models.Model):
    class Meta:
        db_table = 'exchange_goods'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'%s Good ID:%d' % (self.title, self.goods_id)

    goods_id = models.AutoField(primary_key=True)
    type_id = models.IntegerField()
    title = models.CharField(128)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    points = models.IntegerField()
    exchange_counts = models.IntegerField(default=0)
    status = models.IntegerField(default=1)

    @property
    def types(self):
        return ExchangeTypes.objects.get(id=self.type_id)

    @property
    def points_format(self):
        return '{:,.0f}'.format(self.points)

    @property
    def counts_format(self):
        return '{:,.0f}'.format(self.exchange_counts)


# 兑换卡录入
class ExchangeCards(models.Model):
    class Meta:
        db_table = 'exchange_cards'

    connection_name = 'tipshunter'

    def __unicode__(self):
        #return u'%s Good ID:%d' % (self.title, self.goods_id, self.type_id)
        return u'%s Good ID:%d id:%d' % (self.title, self.goods_id, self.id)
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    time = models.DateTimeField()
    end_date = models.DateTimeField()
    changetime = models.DateTimeField()
    goods_id = models.IntegerField()
    #goods_id = ExchangeGoods.objects.get(goods_id)
    type_id = models.IntegerField()
    title = models.CharField(128)
    inprice = models.DecimalField(max_digits=15,decimal_places=2,default=0)
    outprice = models.DecimalField(max_digits=15,decimal_places=2,default=0)
    #title = ExchangeGoods.objects.get(title)
    inprice = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    num = models.CharField(128)
    pwd = models.CharField(128)
    status = models.IntegerField()
    @property
    def Goods(self):
        return ExchangeGoods.objects.get(goods_id=self.goods_id,title=self.title)
    #@property
    #def Types(self):
    #    return ExchangeTypes.objects.get(id=self.types_id,title=self.title)

