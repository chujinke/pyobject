# Iptables
##防火墙
- 主机防火墙：针对于单个主机进行防护。
- 网络防火墙：针对网络入口进行防护，服务于防火墙后的本地局域网。
- 当客户端访问服务器web服务是，信息会通过内核的TCP协议传输到用户空间的web服务中。防火墙的作用是在内核中设置关卡，所有进出的报文都要通过这些关卡，经过检测后，符合放行条件的才被放行，符合阻拦条件的被阻拦。即（input关卡）和（output关卡），在iptables中被称作“链”。
- 当报文经过“链”时，必须和这个关卡上的所有规则匹配一遍。
- 表：相同功能的规则的集合，iptables中定义了4种表：
- - filter表：负责过滤功能，内核模块：iptables_filter
- - nat表：全称（network address translation）网络地址转换功能；内核模块：iptable_nat
- - mangle表:拆解报文，做出修改，并重新封装；内核模块：iptable_mangle
- - raw表：关闭nat表上启用的连接追踪机制；内核模块：iptable_raw
- 四种表优先级（由高到低）：raw > mangle > nat > filter

##规则
- 概念：根据指定的匹配条件来尝试匹配每个流经此处的报文，一旦匹配成功jia将由后面的处理动作进行处理。
- 简单理解 规则 = 匹配条件+处理动作
- 匹配条件：
- - 基本匹配条件：源地址，目标地址
- - 扩展匹配条件
- 处理动作：
- - ACCEPT:允许数据包通过
- - DROP:直接丢弃数据包
- - REJECT:拒绝数据包通过
- - SNAT：源地址转换
- - DNAT:目标地址转换
- - REDIRECT:在本机做端口映射

##Iptabyles
1. netfilter是真的防火墙，位于linux内核。
2. iptables并不是真正的防火墙，是一个命令工具，位于用户空间，可以操作netfilter
3. 规则存储在内核空间的信息过滤表中，这些规则分别指定了源地址，目的地址，传输协议和服务类型等
4. iptables根据规则所定义的方法处理数据包，如放行（accept），拒绝（reject）,丢弃（drop）等。而配置防火墙就是添加、修改、删除、这些规则

##iptables管理规则：
- \-A ：在链尾添加新的规则
- \-I[n]:插入为第n条规则
- \-D ：删除规则
- \-R[n] : 替换第n条
- \-L：显示规则链中已有的条目；
- \-F：清楚规则链中已有的条目；
- \-Z：清空规则链中的数据包计算器和字节计数器；
- \-t<表>：指定要操纵的表；
- \-h：显示帮助信息；
- \-p：指定要匹配的数据包协议类型；
- \-s：指定要匹配的数据包源ip地址；
- \-j<目标>：指定要跳转的目标；
- \-i<网络接口>：指定数据包进入本机的网络接口；
-o<网络接口>：指定数据包要离开本机所使用的网络接口。
```
iptables -t 表名 <-A/I/D/R> 规则链名 [规则号] <-i/o 网卡名> -p 协议名 <-s 源IP/源子网> --sport 源端口 <-d 目标IP/目标子网> --dport 目标端口 -j 动作
```
##命令示例
- 清除已有iptables规则：iptables -F   iptables -Z
- 开放指定的端口：iptables -A INPUT -p tcp --dport 80 -j ACCEPT    #允许访问80端口
- 屏蔽IP：iptables -I INPUT -s 123.0.0.0/8 -j DROP
- 查看已添加的iptables规则：iptables -L -n -v
- 将所有iptables以序号标记显示：iptables -L -n --line-numbers
- 删除INPUT里序号为8的规则：iptables -D INPUT 8
- 使iptables规则生效：iptables-restore < /etc/iptables/rules.v4 

##UFW
1. UFW，即Uncomplicated Firewall，是基于iptables实现的防火墙管理工具，所以实际上UFW修改的是iptables的规则。
2. UFW默认情况下允许所有的出站连接，拒绝所有的入站连接
- sudo ufw default deny incoming
- sudo ufw default allow outgoing
3. 允许SSH连接（一种网络协议，用于计算机之间的加密登录）
- sudo ufw allow ssh = sudo ufw allow 22
4. 查看防火墙状态
- sudo ufw status verbose
5. 查看添加的防火墙规则
- sudo ufw show added
6. 启动UFW
- sudo ufw enable
7. 禁用UFW
- sudo ufw disable
8. 启用防火墙日志：
- sudo ufw logging on
9. 禁用防火墙日志：
- sudo ufw logging off
10. 允许HTTP 80端口的所有连接
- sudo ufw allow http
- sudo ufw allow 80
11. 允许https的连接
- sudo ufw allow https
- sudo ufw allow 443
12. 允许ftp的连接
- sudo ufw allow ftp
- sudo ufw allow 21/tcp
13. 允许指定范围内的端口的指定协议的连接，例如：6000-6007：
- sudo ufw allow 6000:6007/tcp
- sudo ufw allow 6000:6007/udp
14. 允许某IP的所有连接：
- sudo ufw allow from your_ip
15. to any port 22允许端口22的所有连接
- sudo ufw allow from your_ip to any port 22
16. 允许IP段15.15.15.1到15.15.15.254的所有连接：
- sudo ufw allow from 15.15.15.0/24
17.  查看所有规则的规则号
- sudo ufw status numbered
18.  通过规则好删除规则：如果即有ipv6，又有ipv4，那就删除2个
- sudo ufw delete 2
19. 通过规则删除
- sudo ufw delete allow http
- sudo ufw delete allow 80
20. 重置防火墙规则
- sudo ufw reset
21. 批量禁止IP（file.txt是IP列表）
- while read line; do sudo ufw deny from $line; done < file.txt

##DAC和MAC有什么区别
1. DAC（Discretionary Access Control，自主访问控制）
- DAC是传统的Linux的访问控制方式，DAC可以对文件、文件夹、共享资源等进行访问控制。
- 在DAC这种模型中，文件客体的所有者（或者管理员）负责管理访问控制。
- DAC使用了ACL（Access Control List，访问控制列表）来给非管理者用户提供不同的权限，而root用户对文件系统有完全自由的控制权
2. MAC（Mandatory Access Control，强制访问控制）
- SELinux在内核中使用MAC检查操作是否允许。
- 在MAC这种模型中，系统管理员管理负责访问控制，用户不能直接改变强制访问控制属性。
- MAC可以定义所有的进程（称为主体）对系统的其他部分（文件、设备、socket、端口和其它进程等，称为客体）进行操作的权限或许可。
3. DAC和MAC的其它区别
- DAC的主体是真实有效的用户和组ID，MAC的主体是安全上下文，两者的UID是各自独立的。
- DAC的访问控制模式是rwxrwxrwx，MAC的访问控制模式是user:role:type。

## AppArmor与SELinux
1. -  二者相同点：都是Linux中的强制访问控制(Mandatory Access Control)
   - 二者不同点：
       - SELinux太过复杂，apparmor的代码也更易理解和易读。
       - Apparmor使用文件名（路径名）最为安全标签，而SELinux使用文件的inode作为安全标签（在文件系统中，只有inode才具有唯一性）
       - SELinux更安全
2. Apparmor
- Apparmor有两种工作模式
     - Enforcement ： 在这种模式下，配置文件里列出的限制条件都会得到执行，并且对于违反这些限制条件的程序会进行日志记录。
     - Complain ： 在这种模式下，配置文件里的限制条件不会得到执行，Apparmor只是对程序的行为进行记录。





