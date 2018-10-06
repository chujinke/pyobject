#Tornado 

## 1、介绍
> Tornado 是一个Python web框架和异步网络库 起初由 FriendFeed 开发. 通过使用非阻塞网络I/O, Tornado 可以支持上万级的连接，处理 长连接, WebSockets, 和其他 需要与每个用户保持长久连接的应用。
#### Tornado 大体上可以被分为4个主要的部分:

  1. web框架 (包括创建web应用的RequestHandler类，还有很多其他支持的类)     
  2. HTTP的客户端和服务端实现 (HTTPServer and AsyncHTTPClient).
  3. 异步网络库 (IOLoop and IOStream), 为HTTP组件提供构建模块，也可以用来实现其他协议.
  4. 协程库 (tornado.gen) 允许异步代码写的更直接而不用链式回调的方式.
 
## 2、web框架
 1. tornado.web 提供了一种带有异步功能并允许它扩展到大量开放连接的 简单的web 框架,可以处理长连接(long polling) 
    ```
    ##简单示例
    import tornado.ioloop
    import tornado.web
    
    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello, world")
    
    if __name__ == "__main__":
        application = tornado.web.Application([
            (r"/", MainHandler),
        ])
        application.listen(8888)
        tornado.ioloop.IOLoop.current().start()
    ```
 2. **RequestHandler**：HTTP请求处理的基类。
 3. RequestHandler.get_argument(name, default=[], strip=True)：
    >返回指定的name参数的值.<br>
    >如果没有提供默认值, 那么这个参数将被视为是必须的, 并且当 找不到这个参数的时候我们会抛出一个 MissingArgumentError.<br>
    >如果一个参数在url上出现多次, 我们返回最后一个值.<br>
    >返回值永远是unicode.<br>

 4. RequestHandler.get_arguments(name, strip=True):
    > 返回指定name的参数列表.<br>
       如果参数不存在, 返回一个空列表.<br>
       返回值永远是unicode.<br>

 5. RequestHandler.get_query_argument(name, default=[], strip=True)：
    > 从请求的query string返回给定name的参数的值.<br>
    >如果没有提供默认值, 这个参数将被视为必须的, 并且当找不到这个 参数的时候我们会抛出一个 MissingArgumentError 异常.<br>
    >如果这个参数在url中多次出现, 我们将返回最后一次的值.<br>
    >返回值永远是unicode.<br>

 6. RequestHandler.get_query_arguments(name, strip=True):
    > 返回指定name的参数列表.<br>
    >如果参数不存在, 将返回空列表.<br>
    >返回值永远是unicode.<br>

 7. RequestHandler.get_body_argument(name, default=[], strip=True)
    > 返回请求体中指定name的参数的值.<br>
    >如果没有提供默认值, 那么这个参数将被视为是必须的, 并且当    找不到这个参数的时候我们会抛出一个 MissingArgumentError.<br>
    >如果一个参数在url上出现多次, 我们返回最后一个值.<br>
    >返回值永远是unicode.<br>

 8. RequestHandler.get_body_arguments(name, strip=True)
    >返回由指定请求体中指定name的参数的列表.<br>
    >如果参数不存在, 返回一个空列表.<br>
    >返回值永远是unicode.<br>

 9. RequestHandler.request属性和方法:(除非另有说明,所有属性都是str）
    >method:请求方法，例如：“GET” or “POST”<br>
    >uri：请求的uri，例如："/get?type=1&page=1"<br>
    >path：uri中的path，例如：/get<br>
    >query：uri中的query，例如：type=1&page=1<br>
    >version：请求中指定的HTTP版本，例如：HTTP/1.1<br>
    >headers：请求的headers<br>
    >body：请求的body，返回类型是字节串<br>
    >remote_ip：客户端IP<br>
    >protocol：协议类型，例如： “http” or “https”
    >host：请求的主机名，例如：127.0.0.1:8008<br>
    >arguments：获得GET/POST参数，例如：{'type':[b'1'],'page': [b'1']}<br>
    >cookies：cookies，以字典形式出现== RequestHandler.cookies<br>
    >full_url()：重构url，例如:http://127.0.0.1:8008/get?type=1&page=1<br>
    >request_time()：返回执行此请求所需的时间<br>
    >get_ssl_certificate：返回客户端的SSL证书（如果有的话）<br>
    >query_arguments，body_arguments，files，connection<br>

 10. tornado.httputil.url_concat(url, args)：组合URL和参数
 11. tornado.httputil.format_timestamp(ts)：以HTTP使用的格式格式化时间戳。 例子：
     >format_timestamp(1359312200)<br>
     >'Sun, 27 Jan 2013 18:43:20 GMT'

 12. RequestHandler.set_status(status_code, reason=None)：
设置响应的状态码：reason (string) –用人类可读的原因短语来描述状态码
 13. RequestHandler.set_header(name, value):给响应设置指定的头部和对应的值.
 14. RequestHandler.add_header(name, value)：添加指定的响应头和对应的值.
 15. RequestHandler.clear_header(name):清除输出头, 取消之前的 set_header 调用,不适用于被 add_header 设置了多个值的头.
 16. RequestHandler.write(chunk):把给定块写到输出buffer
 17. RequestHandler.flush(include_footers=False, callback=None):将当前输出缓冲区写到网络.
 18. RequestHandler.finish(chunk=None)：完成响应, 结束HTTP 请求.
 19. RequestHandler.render(template_name, **kwargs):使用给定参数渲染模板并作为响应.
 20. RequestHandler.render_string(template_name, **kwargs):使用给定的参数生成指定模板.返回生成的字节字符串(以utf8). 为了生成并写一个模板 作为响应, 使用上面的render()
 21. RequestHandler.get_template_namespace()：返回一个字典被用做默认的模板命名空间.
 22. RequestHandler.redirect(url, permanent=False, status=None):重定向到给定的URL(可以选择相对路径).
 23. RequestHandler.send_error(status_code=500, **kwargs)给浏览器发送指定的HTTP错误码
 24. RequestHandler.clear():重置这个响应的所有头部和内容.
 25. RequestHandler.get_cookie(name, default=None):获取给定name的cookie值, 如果未获取到则返回默认值.
 26. RequestHandler.set_cookie(name, value, domain=None, expires=None, path='/', expires_days=None, **kwargs)：设置给定的cookie 名称/值，和其他
 27. RequestHandler.clear_cookie(name, path='/', domain=None)：删除给定名称的cookie
 28. RequestHandler.clear_all_cookies(path='/', domain=None)：删除用户在本次请求中所有携带的cookie.
 29. RequestHandler.set_secure_cookie(name, value, expires_days=30, version=None, **kwargs)：给cookie签名和时间戳以防被伪造.
 30. RequestHandler.get_secure_cookie(name, value=None, max_age_days=31, min_version=None):如果给定的签名过的cookie是有效的,则返回，否则返回None.

 31. tornado.httputil.parse_request_start_line(line)：例子：
    >parse_request_start_line("GET /foo HTTP/1.1")<br>
    RequestStartLine(method='GET', path='/foo', version='HTTP/1.1')

 32. tornado.httputil.parse_response_start_line(line):例子：
    > parse_response_start_line("HTTP/1.1 200 OK")<br>
    ResponseStartLine(version='HTTP/1.1', code=200, reason='OK')

----------

## tornado.httpserver — 非阻塞 HTTP server
1. tornado.httpserver.HTTPServer(*args, **kwargs)：非阻塞，单线程 HTTP server。
2. 简单的单进程:

    ```
    server = HTTPServer(app)
    server.listen(8888)
    IOLoop.current().start()
    ```
3. 简单的多进程

    ```
    server = HTTPServer(app)
    server.bind(8888)
    server.start(0)  # Fork 多个子进程
    IOLoop.current().start()
    ```
4. 高级多进程

    ```
    sockets = tornado.netutil.bind_sockets(8888)
    tornado.process.fork_processes(0)
    server = HTTPServer(app)
    server.add_sockets(sockets)
    IOLoop.current().start()
    ```
##tornado.httpclient — 异步 HTTP 客户端
1. tornado.httpclient.HTTPClient(async_client_class=None, **kwargs)一个阻塞的 HTTP 客户端.
>close():关闭该 HTTPClient, 释放所有使用的资源.<br>
>fetch(request, **kwargs):执行一个请求, 返回一个 HTTPResponse 对象.

2. class tornado.httpclient.AsyncHTTPClient:一个非阻塞 HTTP 客户端.
>close():销毁该 HTTP 客户端, 释放所有被使用的文件描述符.<br>
>fetch(request, callback=None, raise_error=True, **kwargs)
执行一个请求, 并且异步的返回 HTTPResponse.

    ```
    ##使用示例
    def handle_request(response):
        if response.error:
            print "Error:", response.error
        else:
            print response.body
    
    http_client = AsyncHTTPClient()
    http_client.fetch("http://www.google.com/", handle_request)
    ```
##协同程序和并发
```
##基于回调的异步处理程序
class AsyncHandler(RequestHandler):
    @asynchronous
    def get(self):
        http_client = AsyncHTTPClient()
        http_client.fetch("http://example.com",
                          callback=self.on_fetch)

    def on_fetch(self, response):
        do_something_with_response(response)
        self.render("template.html")
        
##改为协程
class GenAsyncHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("http://example.com")
        do_something_with_response(response)
        self.render("template.html")
        
##生成一个列表或词典Futures的写法
@gen.coroutine
def get(self):
    http_client = AsyncHTTPClient()
    response1, response2 = yield [http_client.fetch(url1),
                                  http_client.fetch(url2)]
    response_dict = yield dict(response3=http_client.fetch(url3),
                               response4=http_client.fetch(url4))
    response3 = response_dict['response3']
    response4 = response_dict['response4']
```
###Future对象：在tornado中大多数的异步操作返回一个Future对象
- 包含了很多属性，包括_result 以及 _callbacks，分别用来存储异步操作的结果以及回调函数
- 包含了很多方法，比如添加回调函数，设置异步操作结果等。
- Future对象对应的异步操作完成后，该对象会被set_done，然后遍历并运行_callbacks中的回调函数。

##tornado.ioloop.IOLoop类
- 利用epoll (Linux) 或者 kqueue (BSD and Mac OS X)水平触发I/O循环

###IOLoop的方法：
- IOLoop.current(instance=True)：返回当前线程的IOLoop
- IOLoop.make_current（）没有当前 IOLoop 时创建的 IOLoop 并自动绑定这个IOLoop
- IOLoop.clear_current() 在当前线程中清除IOLoop
- IOLoop.start()启动当前IOLoop
- IOLoop.stop()停止当前IOLoop
- IOLoop.close（all_fds = False ）关闭IOLoop，释放所有使用的资源

## IO多路复用
1. 文件描述符
- 在unix(like)世界中，一切皆文件（一串二进制流），不管是socket还是管道，都是文件。在信息交换过程中都是对这些二进制流进行数据的收发操作，简称I/O操作，而描述我们操作的哪个流用的是文件描述符（fd）
2. 阻塞
- 非阻塞忙轮询：数据没来，进程就不停地去检测数据，直到数据来
- 阻塞：数据没来，啥都不做，直到数据来，才进行下一步处理。
3. 多个I/O的阻塞
- 如果想同时处理多个socket，可以用非阻塞忙轮询的方式，只要把所有流从头到尾查询一遍，就可以处理多个流了，但是如果所有流都没有I/O事件，就白白浪费CPU时间片。解决方案是不让这个线程亲自去检查是否有I/O事件，而是加一个代理，这个代理检查很多I/O事件，如果没有事件，代理就阻塞，线程就不会轮询了。（select，poll,epoll,kqueue[BSD]）
4. 文件描述符个数限制
- select最大的缺陷就是单个进程所打开的FD是有一定限制的，它由FD_SETSIZE设置，默认值是1024。不能满足拥有万个TCP连接的大型服务器。
- epoll并没有这个限制，它所支持的FD上限是操作系统的最大文件句柄数
5.  I/O效率不会随着FD数目的增加而线性下降的问题
- select/poll每次调用都会线性扫描全部集合，导致效率呈现线性下降，在socket的FD个数很多，活跃的socket很少的情况下效率很低。
- epoll只会对“活跃”的socket进行操作，所以不存在这个问题。
6. 什么是IO多路复用
- 把多个I/O的阻塞复用到同一个select的阻塞上，从而使得系统在单线程的情况下可以同时处理多个客户端请求。与传统的多线程/多进程模型比，I/O多路复用的最大优势是系统开销小，系统不需要创建新的额外进程或者线程，也不需要维护这些进程和线程的运行，降底了系统的维护工作量，节省了系统资源。
7. tornado中的事件池：
- ioloop的configurable_default()：就是根据不同的操作系统返回不同的事件池（linux 就是 epoll， mac 返回 kqueue，其他就返回普通的） select。
- ioloop 实际上是对 epoll的封装，并加入了一些对上层事件的处理和 server 相关的底层处理。



  
  

  




 





