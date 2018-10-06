# Nginx

##Nginx简介
- Nginx 是俄罗斯人编写的十分轻量级的 HTTP 服务器
- Nginx 以事件驱动的方式编写，所以有非常好的性能，同时也是一个非常高效的反向代理、负载平衡。
- 拥有匹敌 Lighttpd 的性能，同时还没有 Lighttpd 的内存泄漏问题，而且 Lighttpd 的 mod_proxy 也有一些问题并且很久没有更新。

##Nginx特点
- 处理静态文件，索引文件以及自动索引；打开文件描述符缓冲．
- 无缓存的反向代理加速，简单的负载均衡和容错．
- FastCGI，简单的负载均衡和容错．
- 模块化的结构。包括 gzipping, byte ranges, chunked responses,以及 SSI-filter 等 filter。如果由 FastCGI 或其它代理服务器处理单页中存在的多个 SSI，则这项处理可以并行运行，而不需要相互等待。
- 支持 SSL 和 TLSSNI．

##Nginx较Apache
- 轻量级，同样起web 服务，比apache 占用更少的内存及资源 
- Nginx 静态处理性能比 Apache 高 
- 抗并发，nginx 处理请求是异步非阻塞的，而apache 则是阻塞型的，在高并发下nginx 能保持低资源低消耗高性能 
- 高度模块化的设计，编写模块相对简单 
- 社区活跃，各种高性能模块出品迅速
- 适合静态和反向。 

##Nginx架构
1. 概要
    - Nginx 在启动后，在 unix 系统中会以 daemon 的方式在后台运行，后台进程包含一个 master 进程和多个 worker 进程。
    - master 进程主要用来管理 worker 进程，包含：接收来自外界的信号，向各 worker 进程发送信号，监控 worker 进程的运行状态，当 worker 进程退出后(异常情况下)，会自动重新启动新的 worker 进程。
    -  worker 进程处理基本网络事件。
    -  一个请求，只可能在一个 worker 进程中处理，一个 worker 进程，不可能处理其它进程的请求。
    -  worker 进程的个数一般设置为机器cpu核数。
    -  每个 worker 里面只有一个主线程，Nginx 采用了异步非阻塞的方式来处理请求解决高并发。
    -  所有 worker 进程在注册 listenfd 读事件前抢 accept_mutex，抢到互斥锁的那个进程注册 listenfd 读事件，在读事件里调用 accept 接受该连接。当一个 worker 进程在 accept 这个连接之后，就开始读取请求，解析请求，处理请求，产生数据后，再返回给客户端，最后才断开连接，这样保证了一个请求，完全由 worker 进程来处理，且只在一个 worker 进程中处理。

    #####这样做的好处：
    - 对于每个 worker 进程来说，独立的进程省掉了锁带来的开销
    - 一个进程退出后，其它进程还在工作，服务不会中断，master 进程则很快启动新的 worker 进程。
    - worker 进程的异常退出，会导致当前 worker 上的所有请求失败，不过不会影响到所有worker请求，所以降低了风险。
2. 负载均衡
- Nginx提供的负载均衡策略有两种：
- - 内置策略：轮询，加权轮询，Ip hash
- - 扩展策略
- Ip hash算法大概原理是：根据请求所属的客户端IP计算得到一个数值，然后把请求发往该数值对应的后端，这样同一个客户端的请求，都会发往同一台后端，除非该后端不可用了，因此ip_hash能够达到保持会话的效果。
3. web缓存
- Nginx可以对不同的文件做不同的缓存处理，配置灵活，并且支持FastCGI_Cache，主要用于对FastCGI的动态程序进行缓存。
4. Nginx配置文件结构
- 全局块：配置影响nginx全局的指令。一般有运行nginx服务器的用户组，nginx进程pid存放路径，日志存放路径，配置文件引入，允许生成worker process数等。
- events块：配置影响nginx服务器或与用户的网络连接。有每个进程的最大连接数，选取哪种事件驱动模型处理连接请求，是否允许同时接受多个网路连接，开启多个网络连接序列化等。
- http块：可以嵌套多个server，配置代理，缓存，日志定义等绝大多数功能和第三方模块的配置。如文件引入，mime-type定义，日志自定义，是否使用sendfile传输文件，连接超时时间，单连接请求数等。
- server块：配置虚拟主机的相关参数，一个http中可以有多个server。
- location块：配置请求的路由，以及各种页面的处理情况。
- 示例如下

    ```
    ########### 每个指令必须有分号结束。#################
    #user administrator administrators;  #配置用户或者组，默认为nobody nobody。
    #worker_processes 2;  #允许生成的进程数，默认为1
    #pid /nginx/pid/nginx.pid;   #指定nginx进程运行文件存放地址
    error_log log/error.log debug;  #制定日志路径，级别。这个设置可以放入全局块，http块，server块，级别以此为：debug|info|notice|warn|error|crit|alert|emerg
    events {
        accept_mutex on;   #设置网路连接序列化，防止惊群现象发生，默认为on
        multi_accept on;  #设置一个进程是否同时接受多个网络连接，默认为off
        #use epoll;      #事件驱动模型，select|poll|kqueue|epoll|resig|/dev/poll|eventport
        worker_connections  1024;    #最大连接数，默认为512
    }
    http {
        include       mime.types;   #文件扩展名与文件类型映射表
        default_type  application/octet-stream; #默认文件类型，默认为text/plain
        #access_log off; #取消服务日志    
        log_format myFormat '$remote_addr–$remote_user [$time_local] $request $status $body_bytes_sent $http_referer $http_user_agent $http_x_forwarded_for'; #自定义格式
        access_log log/access.log myFormat;  #combined为日志格式的默认值
        sendfile on;   #允许sendfile方式传输文件，默认为off，可以在http块，server块，location块。
        sendfile_max_chunk 100k;  #每个进程每次调用传输数量不能大于设定的值，默认为0，即不设上限。
        keepalive_timeout 65;  #连接超时时间，默认为75s，可以在http，server，location块。
    
        upstream mysvr {   
          server 127.0.0.1:7878;
          server 192.168.10.121:3333 backup;  #热备
        }
        error_page 404 https://www.baidu.com; #错误页
        server {
            keepalive_requests 120; #单连接请求上限次数。
            listen       4545;   #监听端口
            server_name  127.0.0.1;   #监听地址       
            location  ~*^.+$ {       #请求的url过滤，正则匹配，~为区分大小写，~*为不区分大小写。
               #root path;  #根目录
               #index vv.txt;  #设置默认页
               proxy_pass  http://mysvr;  #请求转向mysvr 定义的服务器列表
               deny 127.0.0.1;  #拒绝的ip
               allow 172.18.5.54; #允许的ip           
            } 
        }
    }
    ```

5. 概念详解
- worker_connections：表示每个 worker 进程所能建立连接的最大值；一个 Nginx 能建立的最大连接数，应该是worker_connections * worker_processes。
- worker_connections * worker_processes：对于 HTTP 请求本地资源来说，能够支持的最大并发数量
- 如果是 HTTP 作为反向代理来说，最大并发数量应该是worker_connections * worker_processes/2。反向代理服务器里的每个并发会建立与客户端的连接和与后端服务的连接，会占用两个连接。
6. 惊群现象（thundering herd）就是当多个进程和线程在同时阻塞等待同一个事件时，如果这个事件发生，会唤醒所有的进程，但最终只可能有一个进程/线程对该事件进行处理，其他进程/线程会在失败后重新休眠，这种性能浪费就是惊群。
- ngx_accept_disabled作为单个进程负载较高（最大允许连接数的7/8）的标记，计算公式：
ngx_accept_disabled = ngx_cycle->connection_n/8 - ngx_cycle->free_connection_n;
即进程可用连接数free_connection_n小于总连接数connection_n的1/8时ngx_accept_disabled大于0；否则小于0.或者说ngx_accept_disabled小于0时，表示可用连接数较多，负载较低；ngx_accept_disabled大于0时，说明可用连接数较少，负载较高。
- 如果进程负载较低时，即ngx_accept_disabled 小于0，进程允许竞争accept锁。
- 如果进程负载较高时，放弃竞争accept锁，同时ngx_accept_disabled 减1，即认为由于让出一次竞争accept锁的机会，负载稍微减轻
7. 自定义反向代理的错误页面

    ```
    location / {
    # 关键参数：当后端返回404，nginx拦截错误定义错误页面
    proxy_intercept_errors on;
    }
    error_page  404 /404.html;#定义404错误重定向
    location = /404.html {
    root  /usr/share/nginx/html;#存放404.html错误页面的地址
    }
    ```
8. nohup用于使程序在用户退出登陆、关闭终端之后仍能继续运行
- 用法：
     - nohup command
     - exit #（退出nohup模式）
     - ps -ef|grep "command" #（查找运行该命令的进程）
     - kill -9 your_command_pid #(根据进程号关闭程序)
- nohup和&的区别
     - & ： 指在后台运行，但当用户退出(挂起)的时候，命令自动也跟着退出
     - nohup ： 不挂断的运行，注意并没有后台运行的功能，，就是指，用nohup运行命令可以使命令永久的执行下去，和用户终端没有关系，例如我们断开SSH连接都不会影响他的运行
- 例子
     - sh test.sh & ：将sh test.sh任务放到后台 ，关闭xshell，对应的任务也跟着停止。
     - nohup sh test.sh：将sh test.sh任务放到后台，关闭标准输入，终端不再能够接收任何输入（标准输入）
     - nohup sh test.sh  & 将sh test.sh任务放到后台，但是依然可以使用标准输入，终端能够接收任何输入










