#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author lisongjian@youmi.net
#

from django.db import models



# 任务相关
class Mission(models.Model):
    class Meta:
        db_table = 'mission'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%s title:%s' % (self.id, self.title)

    id = models.AutoField(primary_key=True)
    icon = models.CharField(max_length=128)
    desc_url = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    description = models.CharField()
    point =models.IntegerField()
    time_limit =models.IntegerField()
    rest =models.IntegerField()
    status =models.IntegerField()
    stime = models.DateTimeField()
    etime = models.DateTimeField()
    total = models.IntegerField()
    number_limit = models.IntegerField()
    limit = models.IntegerField()


