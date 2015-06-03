# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'you1000.views.home', name='home'),
    # url(r'^you1000/', include('you1000.foo.urls')),

    # 账户模块
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),

    # api接口
    #url(r'^api/', include('apps.api.urls')),

    # 汇总数据
    url(r'^summary/', include('apps.summary.urls')),

    # 用户信息
    url(r'^users/', include('apps.users.urls')),

    # 赚取效果
    url(r'^earns/', include('apps.earns.urls')),

    # 兑换管理
    url(r'^converts/', include('apps.converts.urls')),

    # 系统设置
    url(r'^setting/', include('apps.setting.urls')),

    # 黑名单设置
    url(r'^blacklist/', include('apps.blacklist.urls')),

    # 公告相关
    url(r'^announce/', include('apps.announce.urls')),

    # 应用推广
    url(r'^popularize/', include('apps.popularize.urls')),

    # 任务管理
    url(r'^mission/', include('apps.mission.urls')),

    # 报名管理
    url(r'^go_mission/', include('apps.go_mission.urls')),

     # 积分计算
    url(r'^count_point/', include('apps.count_point.urls')),
   # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
