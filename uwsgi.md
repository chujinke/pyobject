#uwsgi

##概念
- WSGI全称是Web Server Gateway Interface，WSGI不是服务器，是描述web server如何与web application通信的规范。基于[[CGI]]标准而设计的。
- uWSGI：是一个web服务器，实现了WSGI协议、uwsgi协议、http协议等。uWSGI 包括四个部分：
     - uwsgi协议
     - web server 内置支持协议模块
     - application 服务器协议支持模块
     - 进程控制程序
- uwsgi协议是一个uWSGI服务器自有的协议，它用于定义传输信息的类型（type of information），每一个uwsgi packet前4byte为传输信息类型描述。跟fastcgi是最接近的。跟fastcgi的区别在于它是面向多并发的。

##使用Supervisor监控Tornado进程
```
#开启一个进程配置
[program:tornado-0]

# 进程要执行的命令,在虚拟环境中
command=/home/user/website/venv/bin/python server.py --port=8008
directory=/data/web/advance_python/tornado_asyn/#执行文件目录
user=www-data

# 自动重启
autorestart=true
redirect_stderr=true

# 日志路径
stdout_logfile=/var/log/tornado_err.log
loglevel=info

```
- 命令运动 supervisor 服务：
  - supervisord -c /etc/supervisord.conf
- 查看supervisord 是否运行：
 - ps aux|grep supervisord






