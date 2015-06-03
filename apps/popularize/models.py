#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright Youmi 2014
#
# @author lisongjian@youmi.net
#

from django.db import models



# 公告相关
class Popularize(models.Model):
    class Meta:
        db_table = 'popularize'

    connection_name = 'tipshunter'

    def __unicode__(self):
        return u'id:%s content:%s' % (self.id, self.content)

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    content = models.CharField()
    status =models.IntegerField()
    icon = models.CharField(max_length=128)
    url = models.CharField(max_length=512)
    pname = models.CharField(max_length=100)


