#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author lisongjian@youmi.net
#

from django.db import models



# 任务相关
class Go_mission(models.Model):
    class Meta:
        db_table = 'go_mission'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%s uid:%s' % (self.id, self.uid)

    id = models.AutoField(primary_key=True)
    uid =models.IntegerField()
    email = models.CharField()
    lineID = models.CharField()
    mission_id = models.IntegerField()
    status = models.IntegerField()
    stime = models.DateTimeField()
    change_time = models.DateTimeField()
    iv_code = models.CharField()


