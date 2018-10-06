# Redis

## redis和memcached的区别

- Redis和Memcache都是将数据存放在内存中，都是内存数据库。不过memcache还可用于缓存其他东西，例如图片、视频等等；
- Redis不仅仅支持简单的k/v类型的数据，同时还提供list，set，hash等数据结构的存储；
- 虚拟内存--Redis当物理内存用完时，可以将一些很久没用到的value 交换到磁盘；
- 过期策略--memcache在set时就指定，例如set key1 0 0 8,即永不过期。Redis可以通过例如expire 设定，例如expire name 10；
- 分布式--设定memcache集群，利用magent做一主多从;redis可以做一主多从。都可以一主一从；
- 存储数据安全--memcache挂掉后，数据没了；redis可以定期保存到磁盘（持久化）；
- 灾难恢复--memcache挂掉后，数据不可恢复; redis数据丢失后可以通过aof恢复；
- Redis支持数据的备份，即master-slave模式的数据备份；
- value大小-redis最大可以达到1GB，而memcache只有1MB

## Redis 优势

- 性能极高 – Redis能读的速度是110000次/s,写的速度是81000次/s 。
- 丰富的数据类型 – Redis支持二进制案例的 Strings, Lists, Hashes, Sets 及 Ordered Sets 数据类型操作。
- 原子 – Redis的所有操作都是原子性的，意思就是要么成功执行要么失败完全不执行。单个操作是原子性的。多个操作也支持事务，即原子性，通过MULTI和EXEC指令包起来。
- 丰富的特性 – Redis还支持 publish/subscribe, 通知, key 过期等等特性。

## Redis 配置:Redis.conf

```

#是否作为守护进程运行
daemonize yes

#如以后台进程运行，则需指定一个pid，默认为/var/run/redis.pid
pidfile redis.pid

#绑定主机IP，默认值为127.0.0.1
#bind 127.0.0.1

#Redis默认监听端口
port 6379

#客户端闲置多少秒后，断开连接，默认为300（秒）
timeout 300

#日志记录等级，有4个可选值，debug，verbose（默认值），notice，warning
loglevel verbose

#指定日志输出的文件名，默认值为stdout，也可设为/dev/null屏蔽日志
logfile stdout

#可用数据库数，默认值为16，默认数据库为0
databases 16

#保存数据到disk的策略

#当有一条Keys数据被改变是，900秒刷新到disk一次
save 900 1

#当有10条Keys数据被改变时，300秒刷新到disk一次
save 300 10

#当有1w条keys数据被改变时，60秒刷新到disk一次
save 60 10000

#当dump .rdb数据库的时候是否压缩数据对象
rdbcompression yes

#本地数据库文件名，默认值为dump.rdb
dbfilename dump.rdb

#本地数据库存放路径，默认值为 ./
dir /var/lib/redis/
```

## Redis 数据类型

|数据类型|表现形式|数据量|
|:-:|:-:|:-:|
|String|一个key对应一个value|string 类型的值最大能存储 512MB|
|Hash|一个键值对集合|每个hash存储2的32次方-1个键值对（40多亿）|
|List|字符串列表|每个列表最多可存储2的32次方-1个元素|
|Set|string类型的无序集合|每个集合中最大的成员数为2的32次方-1|
|Sorted set|string类型元素的集合|每个集合最大的成员数为2的32次方-1|

## Redis HyperLogLog
- 基数：比如数据集 {1, 3, 5, 7, 5, 7, 8}， 那么这个数据集的基数集为 {1, 3, 5 ,7, 8}, 基数(不重复元素)为5。
- 基数估计就是在误差可接受的范围内，快速计算基数。 

## Redis 发布订阅
- Redis 发布订阅(pub/sub)是一种消息通信模式：发送者(pub)发送消息，订阅者(sub)接收消息。
- Redis 客户端可以订阅任意数量的频道。
- 比如有频道 channel1 ， 以及订阅这个频道的三个客户端 —— client1 、 client2 和 client3 ；当有新消息通过 PUBLISH 命令发送给频道 channel1 时， 这个消息就会被发送给订阅它的三个客户端

## Redis 事务

- Redis 事务可以一次执行多个命令， 并且带有以下重要的保证：
   - 批量操作在发送 EXEC 命令前被放入队列缓存。
   - 收到 EXEC 命令后进入事务执行，事务中任意命令执行失败，其余的命令依然被执行。
   - 在事务执行过程，其他客户端提交的命令请求不会插入到事务执行命令序列中。
- 一个事务从开始到执行会经历以下三个阶段：
   - 开始事务。
   - 命令入队。
   - 执行事务。
- 单个 Redis 命令的执行是原子性的，但 Redis 没有在事务上增加任何维持原子性的机制，所以 Redis 事务的执行并不是原子性的。
- 事务可以理解为一个打包的批量执行脚本，但批量指令并非原子化的操作，中间某条指令的失败不会导致前面已做指令的回滚，也不会造成后续的指令不做。

## redis 提供 6种数据淘汰策略
- voltile-lru：从已设置过期时间的数据集（server.db[i].expires）中挑选最近最少使用的数据淘汰
- volatile-ttl：从已设置过期时间的数据集（server.db[i].expires）中挑选将要过期的数据淘汰
- volatile-random：从已设置过期时间的数据集（server.db[i].expires）中任意选择数据淘汰
- allkeys-lru：从数据集（server.db[i].dict）中挑选最近最少使用的数据淘汰
- allkeys-random：从数据集（server.db[i].dict）中任意选择数据淘汰
- no-enviction（驱逐）：禁止驱逐数据

## 策略规则
- 如果数据呈现幂律分布，即：一部分数据访问频率高，一部分数据访问频率低，则使用allkeys-lru
- 如果数据呈现平等分布，即：所有的数据访问频率都相同，则使用allkeys-random
- 将key设置过期时间实际上会消耗更多的内存，尽量使用allkeys-lru策略从而更有效率的使用内存






