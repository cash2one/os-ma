#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author chenjiehua@youmi.net,lisongjian@youmi.net
#

from django.db import models


class Callback(models.Model):
    """ 回调数据 """
    class Meta:
        db_table = 'callback_order'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'order:%s uid:%u' % (self.order, self.user)

    id = models.AutoField(primary_key=True)
    order = models.CharField(max_length=50)
    oid = models.IntegerField()
    ad = models.CharField(max_length=20)
    adid = models.IntegerField()
    user = models.IntegerField()
    chn = models.IntegerField()
    points = models.IntegerField()
    price = models.FloatField()
    time = models.DateTimeField()
    device = models.CharField(max_length=40)
    sig = models.CharField(max_length=40)
    platform = models.IntegerField()
    ad_source = models.IntegerField()


class AdConfig(models.Model):
    """ 广告配置 """
    class Meta:
        db_table = 'ad_config'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'ad_id:%s description:%s' % (self.ad_id, self.description)

    id = models.AutoField(primary_key=True)
    ad_id = models.IntegerField()
    title = models.CharField(max_length=20)
    intro = models.CharField(max_length=15)
    detail = models.CharField(max_length=100)
    credits = models.CharField(max_length=10)
    icon = models.CharField(max_length=20)
    aos_status = models.BooleanField()
    ios_status = models.BooleanField()
    description = models.CharField(max_length=10)
    priority = models.IntegerField()
