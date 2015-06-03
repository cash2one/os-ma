#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author lisongjian@youmi.net
#

from django.db import models



# 公告相关
class Announce(models.Model):
    class Meta:
        db_table = 'announce'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%s content:%s' % (self.id, self.content)

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.CharField()
    facebook =models.IntegerField()
    online =models.IntegerField()
    url = models.CharField(max_length=100)
    time = models.DateTimeField()
    enddate = models.DateTimeField()
    language = models.IntegerField()

