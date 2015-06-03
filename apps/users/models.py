#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author lisongjian@youmi.net
#

from django.db import models


#用户bind信息
class UserBind(models.Model):
    class Meta:
        db_table = 'user_bind'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'uid:%u token:%s' % (self.uid, self.token)

    uid = models.IntegerField()
    userid = models.CharField()
    token = models.CharField()

# 用户设备
class UserDevices(models.Model):
    class Meta:
        db_table = 'user_device'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'sid:%u fp:%s' % (self.sid, self.fingerprinting)

    sid = models.AutoField(primary_key=True)
    ei = models.CharField(max_length=64)
    si = models.CharField(max_length=64)
    mac = models.CharField(max_length=64)
    andid = models.CharField(max_length=64)
    idfa = models.CharField(max_length=64)
    idfv = models.CharField(max_length=64)
    ser = models.CharField(max_length=64)
    fingerprinting = models.CharField(max_length=64)
    ip = models.CharField()
    cheat = models.IntegerField()
    type = models.IntegerField()

# 用户信息
class Users(models.Model):
    class Meta:
        db_table = 'user'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'user:%s uid:%u' % (self.scopeid, self.uid)

    uid = models.AutoField(primary_key=True)
    scopeid = models.CharField(max_length=20)
    gender = models.CharField(max_length=8)
    name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    create_at = models.DateTimeField()
    phone = models.CharField(max_length=11)
    alipay = models.CharField(max_length=25)
    points = models.IntegerField()
    ex_points = models.IntegerField()
    invite_points = models.IntegerField()
    total_points = models.IntegerField()
    sign_days = models.IntegerField()
    invited_by = models.IntegerField()
    invited_code = models.CharField()
    invites = models.IntegerField()
    locale = models.CharField()
    last_login = models.DateTimeField()
    token = models.CharField(max_length=64)
    platform = models.CharField()
    star_gg = models.IntegerField()
    ip = models.CharField()
    appType = models.IntegerField()
    mail = models.CharField()
    version = models.CharField()
    wonder = models.IntegerField()
    en = models.IntegerField()
    ad_from = models.IntegerField()
    utm_source = models.CharField()

    @property
    def user_device(self):
        #return UserDevices.objects.get(uid=self.uid)
        return UserBind.objects.get(uid=self.uid)[:1]


# 用户签到
class UserSign(models.Model):
    class Meta:
        db_table = 'user_sign'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'uid:%s time:%s grade:%s' % (self.uid, self.time)

    id = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    time = models.DateTimeField()


# 全局订单
class GlobalOrders(models.Model):
    class Meta:
        db_table = 'global_orders'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'uid:%s note:%s' % (self.uid, self.note)

    id = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    points = models.IntegerField()
    last = models.IntegerField()
    record_time = models.DateTimeField()
    type = models.IntegerField()
    note = models.CharField()

    @property
    def user(self):
        #return UserDevices.objects.get(uid=self.uid)
        return Users.objects.get(uid=self.uid)

# 全局订单
class CallbackOrders(models.Model):
    class Meta:
        db_table = 'callback_order'

    connection_name = 'tipshunter'

    id = models.AutoField(primary_key=True)
    order = models.CharField()
    oid = models.IntegerField()
    ad = models.CharField()
    user = models.IntegerField()
    points = models.IntegerField()
    platform = models.IntegerField()
    ad_source = models.IntegerField()
    time = models.DateTimeField()

#app list信息
class appList(models.Model):
    class Meta:
        db_table = 'app_list'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%u name:%s' % (self.id, self.name)

    id = models.IntegerField()
    name = models.CharField()

