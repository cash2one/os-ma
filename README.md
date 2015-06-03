git init
git clone ```
## 目录说明

- - -

```
* config/          // 配置
* assets/          // 静态资源
* apps/            // 具体页面
* apps/templates/  // 模板
```

## 环境搭建

```
pip install -r requirements.txt
```

## 本地运行说明

1. 复制配置文件 config/setting.py，并修改配置文件对应项
2. 根目录执行 ``python manage.py runserver 0.0.0.0:8000`` ，访问 `http://127.0.0.1:8000` 即可，或者配置域名访问，流程参考部署流程


## 测试帐号

[admin地址1](http://admin.cc/) 
[admin地址2](http://admin.hk/) 
### 远程访问 
* sudo vim /etc/hosts 
* 加一行：   203.90.236.185 admin.hk admin.cc
* 访问地址 admin.cc admin.hk 用户名youmi
* 密码 ILoveYoumi@Haiwai123



## 部署上线说明

### Configure

1. 配置文件 'config/setting.py'修改配置文件对应项
2. 关闭debug模式

```python
DEBUG = False
```

### Init Database

```
cd ../manager
python manage.py syncdb --database=default
```

* [参考地址](http://djangobook.py3k.cn/2.0/chapter06/)

### nginx 配置参考
* cd /etc/nginx/sites-enabled
* vim TipsHunterManager
* Run with Nginx

```
server {
        server_name             admin.cc admin.hk;
        rewrite_log             on;
        charset                 utf8;

        root /home/ubuntu/vhost/overseas/manager;

        location /assets {
                access_log off;
                expires 30d;
        }

        location / {
                include     uwsgi_params;
                uwsgi_pass  127.0.0.1:3034;
        }
}
```

service nginx reload

### uWSGI 配置参考

cd /etc/uwsgi/apps-enabled
vim TipsHunterManager.ini
```
[uwsgi]
socket = 0.0.0.0:3034
chdir = /home/ubuntu/vhost/overseas/manager
home = /home/ubuntu/virtualenv/oversea
module = config.wsgi
```


service uwsgi restart

