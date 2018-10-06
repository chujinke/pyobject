# HTTP笔记

##HTTP介绍
- HTTP协议（HyperText Transfer Protocol，超文本传输协议）是用于从WWW服务器传输超文本到本地浏览器的传输协议。它可以使浏览器更加高效，使网络传输减少。它不仅保证计算机正确快速地传输超文本文档，还确定传输文档中的哪一部分，以及哪部分内容首先显示(如文本先于图形)等
- HTTP 是基于 TCP/IP 协议的应用层协议。它不涉及数据包（packet）传输，主要规定了客户端和服务器之间的通信格式，默认使用80端口。
- 浏览器请求流程：
    - 域名解析 -->
    - 发起TCP的3次握手 -->
    - 建立TCP连接后发起http请求 -->
    - 服务器响应http请求，浏览器得到html代码 -->
    - 浏览器解析html代码，并请求html代码中的资源（如js、css等） -->
    - 浏览器对页面进行渲染呈现给用户
- 为什么HTTP协议要基于TCP来实现？
    - TCP是一个端到端的可靠的面向连接的协议，所以HTTP基于传输层TCP协议不用担心数据的传输的各种问题。
    - 建立TCP连接后发起http请求

##HTTP版本
1. HTTP/0.9
- 1991年发布，只有GET请求
- 服务器只能回应HTML格式的字符串，不能回应别的格式。
- 服务器发送完毕，就关闭TCP连接。
2. HTTP/1.0
- 1996年5月发布，任何格式的内容都可以发送。
- 引入了POST命令和HEAD命令
- 增加请求头（HTTP header）
- 还新增包括状态码（status code）、多字符集支持、多部分发送（multi-part type）、权限（authorization）、缓存（cache）、内容编码（content encoding）等。
3. HTTP/1.1
- 1997年1月发布
- 主要是引入了持久连接（persistent connection），即TCP连接默认不关闭，可以被多个请求复用，不用声明Connection: keep-alive。
- 目前，对于同一个域名，大多数浏览器允许同时建立6个持久连接。
- 引入了管道机制（pipelining），即在同一个TCP连接里面，客户端可以同时发送多个请求。
- PUT、PATCH、HEAD、 OPTIONS、DELETE。
4. SPDY 协议
- 2009年，谷歌公开了自行研发的 SPDY 协议
- HTTP/2 继承了它很多特性。
5. HTTP/2
- 2015年，HTTP/2 发布。它不叫 HTTP/2.0，是因为标准委员会不打算再发布子版本了，下一个新版本将是 HTTP/3。
- 头信息和数据体都是二进制，并且统称为"帧"（frame）：头信息帧和数据帧。
- 在一个连接里，客户端和浏览器都可以同时发送多个请求或回应，而且不用按照顺序一一对应，这样就避免了"队头堵塞"。
- 将每个请求或回应的所有数据包，称为一个数据流（stream）。每个数据流都有一个独一无二的编号。数据包发送的时候，都必须标记数据流ID，用来区分它属于哪个数据流。另外还规定，客户端发出的数据流，ID一律为奇数，服务器发出的，ID为偶数。
- 客户端还可以指定数据流的优先级。优先级越高，服务器就会越早回应。
- 头信息使用gzip或compress压缩后再发送；另一方面，客户端和服务器同时维护一张头信息表，所有字段都会存入这个表，生成一个索引号，以后就不发送同样字段了，只发送索引号，
- 允许服务器未经请求，主动向客户端发送资源，这叫做服务器推送（server push）。

##URL
>schema://host[:port#]/path/.../[;url-params][?query-string][#anchor]

- scheme：指定低层使用的协议，一般是http，如果强调安全的话可以是https
- host：HTTP服务器的IP地址或者域名
- port：HTTP服务器的默认端口是80，这种情况下端口号可以省略。如果使用了别的端口，必须指明
- path：访问资源的路径
- url-params：URL的参数，例如：id=8079
- query-string：发送给http服务器的数据
- anchor：锚
##客户端请求消息
- 请求行：请求方法空格URL空格协议版本换行
- 请求头
- 空行
- 请求数据
##服务器响应消息
- 状态行：协议版本空格状态码空格状态描述信息换行
- 消息报头
- 空行
- 响应正文
##HTTP常见的请求头
- If-Modified-Since：把浏览器端缓存页面的最后修改时间发送到服务器去，服务器会把这个时间与服务器上实际文件的最后修改时间进行对比。如果时间一致，那么返回304，客户端就直接使用本地缓存文件。如果时间不一致，就会返回200和新的文件内容。客户端接到之后，会丢弃旧文件，把新文件缓存起来，并显示在浏览器中。
- If-None-Match：If-None-Match和ETag一起工作，工作原理是在HTTP Response中添加ETag信息。 当用户再次请求该资源时，将在HTTP Request 中加入If-None-Match信息(ETag的值)。如果服务器验证资源的ETag没有改变（该资源没有更新），将返回一个304状态告诉客户端使用本地缓存文件。否则将返回200状态和新的资源和Etag.  使用这样的机制将提高网站的性能。
- Pragma：指定“no-cache”值表示服务器必须返回一个刷新后的文档，即使它是代理服务器而且已经有了页面的本地拷贝；在HTTP/1.1版本中，它和Cache-Control:no-cache作用一模一样。Pargma只有一个用法， 例如： Pragma: no-cache。注意: 在HTTP/1.0版本中 没有实现Cache-Control
- Cache-Control：指定请求和响应遵循的缓存机制。
- Accept：浏览器端可以接受的MIME类型。例如 Accept: */* 代表浏览器可以处理所有类型
- Accept-Encoding：浏览器申明自己可接收的编码方法，通常指定压缩方法，是否支持压缩，支持什么压缩方法（gzip，deflate）
- Accept-Language：浏览器申明自己接收的语言。
- Accept-Charset：浏览器可接受的字符集。
- User-Agent：告诉HTTP服务器，客户端使用的操作系统和浏览器的名称和版本。
- Content-Type：用于定义网络文件的类型和网页的编码，决定浏览器将以什么形式、什么编码读取这个文件。
- Referer：包含一个URL，用户从该URL代表的页面出发访问当前请求的页面。
- Connection: keep-alive 当一个网页打开完成后，客户端和服务器之间用于传输HTTP数据的TCP连接不会关闭，如果客户端再次访问这个服务器上的网页，会继续使用这一条已经建立的连接。HTTP 1.1默认进行持久连接。
- Connection: close 代表一个Request完成后，客户端和服务器之间用于传输HTTP数据的TCP连接会关闭，当客户端再次发送Request，需要重新建立TCP连接。
- Host：（发送请求时，该头域是必需的）主要用于指定被请求资源的Internet主机和端口号，它通常从HTTP URL中提取出来的。HTTP/1.1请求必须包含主机头域，否则系统会以400状态码返回。
- Cookie：将cookie的值发送给HTTP服务器。
- Content-Length：表示请求消息正文的长度。
- Authorization：授权信息
- From：请求发送者的email地址，由一些特殊的Web客户程序使用，浏览器不会用到它。

##HTTP常见的响应头
- Allow：服务器支持哪些请求方法（如GET、POST等）
- Date：表示消息发送的时间，时间的描述格式由rfc822定义。例如，Date:Mon,31Dec200104:25:57GMT。
- Expires：指明应该在什么时候认为文档已经过期，从而不再缓存它，重新从服务器获取，会更新缓存。过期之前使用本地缓存。HTTP1.1的客户端和缓存会将非法的日期格式（包括0）看作已经过期。
   - eg：为了让浏览器不要缓存页面，我们也可以将Expires实体报头域，设置为0。
   - 例如: Expires: Tue, 08 Feb 2022 11:35:14 GMT
- P3P：用于跨域设置Cookie, 这样可以解决iframe跨域访问cookie的问题
- Set-Cookie：用于把cookie发送到客户端浏览器。
- ETag：和If-None-Match 配合使用。
- Last-Modified：用于指示资源的最后修改日期和时间。Last-Modified也可用setDateHeader方法来设置。
- Content-Type：WEB服务器告诉浏览器自己响应的对象的类型和字符集。
- Content-Length：指明实体正文的长度，以字节方式存储的十进制数字来表示。
- Content-Encoding：WEB服务器表明自己使用了什么压缩方法（gzip，deflate）压缩响应中的对象。
- Content-Language：WEB服务器告诉浏览器自己响应的对象所用的自然语言。
- Server：指明HTTP服务器用来处理请求的软件信息。
- X-Powered-By：表示网站是用什么技术开发的。例如： X-Powered-By: ASP.NET
- Connection：keep-alive/close
- Location：用于重定向一个新的位置，包含新的URL地址。
- Refresh：表示浏览器应该在多少时间之后刷新文档，以秒计。不属于HTTP 1.1正式规范，Netscape和IE支持
- WWW-Authenticate：该响应报头域必须被包含在401（未授权的）响应消息中，客户端收到401响应消息时候，并发送Authorization报头域请求服务器对其进行验证时，服务端响应报头就包含该报头域。

##HTTPS传输协议原理
1. HTTPS（全称：Hypertext Transfer Protocol over Secure Socket Layer），是以安全为目标的HTTP通道，简单讲是HTTP的安全版。
2. HTTP下加入SSL层，HTTPS的安全基础是SSL
    - HTTP|TCP|IP
    - HTTPS|SSL or TLS|TCP|IP
    - SSL（Secure Socket Layer，安全套接字层）
    - TLS（Transport Layer Security，传输层安全）
3. 优点：
    - HTTP + 加密 + 认证 + 完整性保护 = HTTPS
    - 客户端产生的密钥只有客户端和服务器端能得到；
    - 加密的数据只有客户端和服务器端才能得到明文；
    - 客户端到服务端的通信是安全的。
    - 具有校验机制，一旦被篡改，通信双方会立刻发现。
    - 配备身份证书，防止身份被冒充。



