#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


# 回调数据
class Callback(models.Model):
    class Meta:
        db_table = 'callback_order'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'order:%s uid:%u' % (self.order, self.user)

    order = models.CharField(max_length=50)
    oid = models.IntegerField()
    ad = models.CharField(max_length=20)
    adid = models.IntegerField()
    user = models.IntegerField()
    chn = models.IntegerField()
    points = models.IntegerField()
    price = models.FloatField()
    time = models.DateTimeField(null=True, blank=True)
    device = models.CharField(max_length=40)
    sig = models.CharField(max_length=40)
    platform = models.IntegerField()
    ad_source = models.IntegerField()
    appType = models.IntegerField()

class Income(models.Model):
    class Meta:
        db_table = 'income'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%s day:%u' % (self.id, self.day)

    id = models.IntegerField()
    day = models.DateTimeField(null=True, blank=True)
    youmi = models.DecimalField(max_digits=10, decimal_places=3)
    adxmi = models.DecimalField(max_digits=10, decimal_places=3)
    vungle = models.DecimalField(max_digits=10, decimal_places=3)
    supersonic = models.DecimalField(max_digits=10, decimal_places=3)
    aarki = models.DecimalField(max_digits=10, decimal_places=3)
    adcolony = models.DecimalField(max_digits=10, decimal_places=3)
    trialpay = models.DecimalField(max_digits=10, decimal_places=3)
    fyber = models.DecimalField(max_digits=10, decimal_places=3)
    metaps = models.DecimalField(max_digits=10, decimal_places=3)
    appdriver = models.DecimalField(max_digits=10, decimal_places=3)
    admob = models.DecimalField(max_digits=10, decimal_places=3)
    duomeng = models.DecimalField(max_digits=10, decimal_places=3)
    dincome = models.DecimalField(max_digits=10, decimal_places=3)
    rincome = models.DecimalField(max_digits=10, decimal_places=3)
    cost = models.DecimalField(max_digits=10, decimal_places=3)
    gprofit = models.DecimalField(max_digits=10, decimal_places=3)
    gmargin = models.FloatField()
    duiba_cost = models.DecimalField(max_digits=10, decimal_places=3)
    paypal_cost = models.DecimalField(max_digits=10, decimal_places=3)
    dollar = models.DecimalField(max_digits=5, decimal_places=3)
    self_cost = models.DecimalField(max_digits=10, decimal_places=3)
    woobi = models.DecimalField(max_digits=10, decimal_places=3)
    airpush = models.DecimalField(max_digits=10, decimal_places=3)
    personaly = models.DecimalField(max_digits=10, decimal_places=3)
