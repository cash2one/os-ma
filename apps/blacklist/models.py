#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author chenjiehua@youmi.net
#

from django.db import models


# 黑名单
class Iplist(models.Model):
    class Meta:
        db_table = 'ip_blacklist'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%s ip:%s' % (self.id, self.ip)

    id = models.AutoField(primary_key=True)
    status =models.IntegerField()
    ip = models.CharField(max_length=50)
    note = models.CharField()

class Maillist(models.Model):
    class Meta:
        db_table = 'mail_blacklist'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%s mail:%s' % (self.id, self.mail)

    id = models.AutoField(primary_key=True)
    mail = models.CharField(max_length=50)
    status =models.IntegerField()
    note = models.CharField()

class Idfalist(models.Model):
    class Meta:
        db_table = 'idfa_blacklist'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%s idfa:%s' % (self.id, self.idfa)

    id = models.AutoField(primary_key=True)
    status =models.IntegerField()
    idfa = models.CharField(max_length=50)
    note = models.CharField()

class Imeilist(models.Model):
    class Meta:
        db_table = 'imei_blacklist'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%s imei:%s' % (self.id, self.imei)

    id = models.AutoField(primary_key=True)
    imei = models.CharField(max_length=50)
    status =models.IntegerField()
    note = models.CharField()

class Uidlist(models.Model):
    class Meta:
        db_table = 'user_blacklist'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%s uid:%s' % (self.id, self.uid)

    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=50)
    note = models.CharField()
    status =models.IntegerField()
