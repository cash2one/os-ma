#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author chenjiehua@youmi.net
#

from django.db import models


# 广告配置
class AdConfig(models.Model):
    class Meta:
        db_table = 'ad_config'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'ad_id:%d title:%s' % (self.ad_id, self.title)

    id = models.AutoField(primary_key=True)
    ad_id = models.IntegerField()
    title = models.CharField(max_length=20)
    intro = models.CharField(max_length=15)
    detail = models.CharField(max_length=100)
    credits = models.CharField(max_length=10)
    icon = models.CharField(max_length=20)
    aos_status = models.IntegerField()
    ios_status = models.IntegerField()
    description = models.CharField(max_length=10)
    priority = models.IntegerField()
    iospriority = models.IntegerField()
    exchangeRate = models.FloatField()
    pname = models.CharField()

# 选项设置
class Options(models.Model):
    class Meta:
        db_table = 'options'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'key:%s values:%s' % (self.key, self.description)

    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=20)
    values = models.IntegerField()
    description = models.CharField(max_length=20)

# 帮抢高价
class Recommend(models.Model):
    class Meta:
        db_table = 'task_recommend'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%d title:%s' % (self.id, self.title)

    id = models.AutoField(primary_key=True)
    ad_id = models.IntegerField()
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=150)
    points = models.IntegerField()
    status = models.IntegerField()

    @property
    def ad(self):
        return AdConfig.objects.get(ad_id=self.ad_id)

# 选项设置
class Feedback(models.Model):
    class Meta:
        db_table = 'feedback'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%s content:%s' % (self.id, self.content)

    id = models.AutoField(primary_key=True)
    status =models.IntegerField()
    user = models.IntegerField()
    content = models.CharField(max_length=20)
    mail = models.CharField(max_length=20)
    time = models.DateTimeField()
    scopeid = models.CharField(max_length=20)
    appType = models.IntegerField()


# 每日奖励
class Daily(models.Model):
    class Meta:
        db_table = 'daily_reward'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%s title:%s' % (self.id, self.title)

    id = models.AutoField(primary_key=True)
    ad_id = models.IntegerField()
    title = models.CharField()
    description = models.CharField()
    total_task = models.IntegerField()
    points = models.IntegerField()
    status = models.IntegerField()
