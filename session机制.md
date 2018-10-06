# session机制

## cookie
- Cookie是由服务器发给客户端的特殊信息，而这些信息以文本文件的方式存放在客户端，然后客户端每次向服务器发送请求的时候都会带上这些特殊的信息。即：当用户使用浏览器访问一个支持Cookie的网站的时候，用户会提供包括用户名在内的个人信息并且提交至服务器；接着，服务器在向客户端回传相应的超文本的同时也会发回这些个人信息，当然这些信息并不是存放在HTTP响应体（Response Body）中的，而是存放于HTTP响应头（Response Header）；当客户端浏览器接收到来自服务器的响应之后，浏览器会将这些信息存放在一个统一的位置。
- 客户端再向服务器发送请求的时候，都会把相应的Cookie再次发回至服务器。这次Cookie信息则存放在HTTP请求头（Request Header）。
- 利用Cookie技术，服务器在接收到来自客户端浏览器的请求之后，能够通过分析存放于请求头的Cookie得到客户端特有的信息，从而动态生成与该客户端相对应的内容。
- 例如：网站的登录界面中的“请记住我”，如果你勾选了它之后再登录，在下一次访问该网站的时候就不需要进行重复而繁琐的登录动作了
- cookie的内容主要包括：名字，值，过期时间，路径和域。 

## session

- session技术是服务端的解决方案。把客户端浏览器与服务器之间一系列交互的动作称为一个 Session。
- 使用Session步骤：
   - 创建Session。不同后台语言实现的应用程序有不同创建Session的方法
   - 在创建了Session的同时，服务器会为该Session生成唯一的Sessionid，而Sessionid在随后的请求中会被用来重新获得已经创建的Session；
   - 在Session被创建之后，调用Session相关的方法往Session中增加内容了，这些内容只会保存在服务器中，发到客户端的只有Sessionid；
   - 当客户端再次发送请求的时候，会将这个Sessionid带上，服务器接受到请求之后就会依据Sessionid找到相应的Session，从而再次使用之。

## cookie与session的关系
- cookie和session的方案虽然分别属于客户端和服务端。
- 服务端的session的实现对客户端的cookie是有依赖关系，服务端执行session机制时候会生成session的id值，这个id值会发送给客户端，客户端每次请求都会把这个id值放到http请求的头部发送给服务端，而这个id值在客户端会保存下来，保存的容器是cookie
- 当我们完全禁掉浏览器的cookie的时候，服务端的session是不能正常使用的

## cookie 和session 的区别：
- cookie数据存放在客户的浏览器上，session数据放在服务器上。
- cookie不是很安全，别人可以分析存放在本地的COOKIE并进行COOKIE欺骗
   考虑到安全应当使用session。
- session会在一定时间内保存在服务器上。当访问增多，会比较占用你服务器的性能
   考虑到减轻服务器性能方面，应当使用COOKIE。
- 单个cookie保存的数据不能超过4K，很多浏览器都限制一个站点最多保存20个cookie。

## nginx反向代理中的session问题
- 问题
   - 当nginx做反向代理，负载均衡时，连接会被负载到不同服务器，在一个服务器建立的session不能被另一个服务器读取
   - 例如：在服务器一登录后，而跳转到首页的时候，负载到了服务器二，而服务器二并没有服务器一的登录信息，又会需要登录，这样可能会出现登录死循环。
- 解决方案
   - 利用ip_hash负载，请求来的相同ip会请求固定的一台服务器，但是一个局域网下，所有链接会分发到一台服务器，也有可能造成负载失衡。

## session 的数据保存
- Django
  - 路径： '/'是Django安装的URL路径或是该路径的父级。
  - 时间：1209600秒（两周）
- tomcat的StandardManager类将session存储在内存中，也可以持久化到file，数据库，memcache，redis等。
- 客户端只在cookie中保存sessionid，而不会保存session，session销毁只能通过invalidate或超时，关掉浏览器并不会关闭session。

## 通用的多台服务器共享session问题
|解决方案|缺点|
|:-:|:-:|
|通过数据库mysql共享session|a:用专门的数据库服务器，如果服务器不能正常工作会影响整体；<br>b:和业务数据库用一个会增加数据库负担，而且session查询频率很高|
|通过cookie共享session|cookie的安全性不高，容易伪造、客户端禁止使用cookie等都可能造成无法共享session。|
|通过服务器之间的数据同步session|速度慢，同步session有延迟性|
|通过memcache同步session|memcache不能完全利用内存，会产生内存碎片，如果存储块不足，还会产生内存溢出。 |
|通过redis共享session|暂无|





