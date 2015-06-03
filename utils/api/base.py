#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author    lijinsheng@youmi.net
#
from datetime import tzinfo, timedelta

UTC_TIME = timedelta(0)
LOCAL_TIME = timedelta(hours=8)

class UTC(tzinfo):
    def utcoffset(self, dt):
        return UTC_TIME

    def dst(self, dt):
        return UTC_TIME

class LOCAL(tzinfo):
    def utcoffset(self, dt):
        return LOCAL_TIME

    def dst(self, dt):
        return LOCAL_TIME

    def tzname(self, dt):
        return "+08:00"
