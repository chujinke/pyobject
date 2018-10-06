#Django

## Django和Tornado
- Django
    - 注重高效开发
    - 全自动化的管理后台（只需要使用起ORM，做简单的定义，就能自动生成数据库结构，全功能的管理后台）
    - session功能
- Tornado
    - 注重性能优越，速度快
    - 解决高并发
    - 异步非阻塞
    - websockets 长连接
    - 内嵌了HTTP服务器
    - 单线程的异步网络程序，默认启动时根据CPU数量运行多个实例；利用CPU多核的优势。
## Django目录结构
- 目录说明：
    - HelloWorld: 项目的容器。
    - manage.py: 一个实用的命令行工具，可让你以各种方式与该 Django 项目进行交互。
    - HelloWorld/__init__.py: 一个空文件，告诉 Python 该目录是一个 Python 包。
    - HelloWorld/settings.py: 该 Django 项目的设置/配置。
    - HelloWorld/urls.py: 该 Django 项目的 URL 声明; 一份由 Django 驱动的网站"目录"。
    - HelloWorld/wsgi.py: 一个 WSGI 兼容的 Web 服务器的入口，以便运行你的项目。
- 应用目录
    - App/
       - __init__.py
       - admin.py
       - apps.py
       - migrations/
           - \__init__.py
       - models.py
       - tests.py
       - views.py
       - urls.py

## Django相关命令及其作用
|命令|作用|
|:-:|:-:|
|python -m django --version|查看Django版本|
|django-admin startproject HelloWorld|创建项目|
|python manage.py makemigrations|创建更改数据库文件|
|python manage.py migrate|创建数据库表|
|python manage.py flush|清空数据库|
|python manage.py runserver|运行项目|
|python manage.py startapp App|创建应用|
|python manage.py createsuperuser|创建超级用户|
|python manage.py changepassword username|修改密码|
|python manage.py shell|交互式 Python 命令行|
|python manage.py dbshell|数据库命令行|

## 模型
- 模型是数据唯一而且准确的信息来源。一般，每一个模型都映射一个数据库表。
- 概要：
    - 每个模型都是一个 Python 的类，这些类继承 django.db.models.Model
    - 模型类的每个属性都相当于一个数据库的字段。
- 代码示例
```
	from django.db import models

	class Person(models.Model):
		name = models.CharField(max_length=30)
		age = models.IntegerField()
```
## 字段类型
|类型|描述|必须传入参数|
|:-:|:-:|:-:|
|AutoField|根据 ID 自增长的 IntegerField 字段||
|IntegerField|整数字段||
|BigIntegerField|64位整数||
|BooleanField|布尔值字段||
|CharField|字符串字段|max_length|
|CommaSeparatedInterField|存放以逗号间隔的整数序列|max_length|
|DateField|日期字段|auto_now=False修改时间，auto_now_add=False创建时间|
|DateTimeField|日期和时间|参数同上|
|DecimalField|固定精度数|max_digits数字最大位数，decimal_places小数最大位数|
|EmailField|email合法性检测字段|max_length默认75，兼容所有254|
|FileField|文件上传字段|upload_to：保存文件的本地文件系统|
|FloatField|浮点数||
|ImageField|会验证上传对象是不是一个合法的图象文件||
|IPAddressField|以字符串形式表示 IP 地址字段||
|GenericIPAddressField|同上，增加ipv6||
|NullBooleanField|同BooleanField 多了NULL 选项||
|PositiveIntegerField|和 IntegerField 相似，必须是非负数。||
|TextField|大文本字段||
|TimeField|时间||
|URLField|保存 URL 的 CharField 。||

- 添加应用
   - 将新建的应用（App）添加到 settings.py 中的 INSTALLED_APPS中
- 插入数据
```
	Author.objects.create(name="", email="")
	# 方法 2
	twz = Author(name="", email="")
	twz.save()
	# 方法 3
	twz = Author()
	twz.name=""
	twz.email=""
	twz.save()
	# 方法 4，首先尝试获取，不存在就创建，可以防止重复
	Author.objects.get_or_create(name="", email="")
	# 返回值(object, True/False)
```

- 查询数据

```
	Person.objects.all() # 查询所有
	Person.objects.all()[:10] 切片操作，获取10个人，不支持负索引，切片可以节约内存，不支持负索引，后面有相应解决办法，第7条
	Person.objects.get(name="WeizhongTu") # 名称为 WeizhongTu 的一条，多条会报错

	get是用来获取一个对象的，如果需要获取满足条件的一些人，就要用到filter
	Person.objects.filter(name="abc") # 等于Person.objects.filter(name__exact="abc") 名称严格等于 "abc" 的人
	Person.objects.filter(name__iexact="abc") # 名称为 abc 但是不区分大小写，可以找到 ABC, Abc, aBC，这些都符合条件

	Person.objects.filter(name__contains="abc") # 名称中包含 "abc"的人
	Person.objects.filter(name__icontains="abc") #名称中包含 "abc"，且abc不区分大小写

	Person.objects.filter(name__regex="^abc") # 正则表达式查询
	Person.objects.filter(name__iregex="^abc")# 正则表达式不区分大小写

	# filter是找出满足条件的，当然也有排除符合某条件的
	Person.objects.exclude(name__contains="WZ") # 排除包含 WZ 的Person对象
	Person.objects.filter(name__contains="abc").exclude(age=23) # 找出名称含有abc, 但是排除年龄是23岁的
```
- QuerySet API：从数据库中查询出来的结果一般是一个集合

|语法|作用|
|:-:|:-:|
|Person.objects.create(name="路飞", age=20)|插入数据|
|Person.objects.create(name="路飞", age=20)|插入数据|
|Person.objects.get(name="路飞")|查询语句|
|Person.objects.all()[:10] |获取10个人，不支持负索引|
|Person.objects.all().reverse()[:2]|最后两条|
|qs = qs.distinct()|结果去重|
|Person.objects.filter(name__exact="abc") |name严格等于“abc”|
|Person.objects.filter(name__iexact="abc") |name等于“abc”,不区分大小写|
|Person.objects.filter(name__contains="abc") |name包含“abc”|
|Person.objects.filter(name__regex="^abc") |正则|
|Person.objects.exclude(name__contains="路飞")|排除包含路飞的Person对象|
|Person.objects.filter(name__contains="abc").exclude(age=23)|找出名称含有abc, 但是排除年龄是23岁的|
|Person.objects.filter(name__contains="abc").delete()|删除name包含“abc”|
|Person.objects.filter(name__contains="abc").update(name='xxx')|名称中包含 "abc"的人 都改成 xxx|
|Person.objects.all().order_by('-name')|排序，加-号代表倒序|
|Person.objects.values_list('name', 'age')|元组形式的结果|
|Person.objects.values('name', 'age')|字典形式的结果|

## 视图（App目录下的views.py）

- 代码示例

	```
		def detail(request, id):
			return HttpResponse("Hello %s." % id)
	```
- HttpRequest 对象

|属性/方法|作用|示例|
|:-:|:-:|:-:|
|scheme|表示请求的方案|字符串（http/https）|
|body|原始的http请求正文|一个字节字符串|
|path|请求路径|字符串 "/music/100"|
|method|请求方法|大写字符串（GET/POST）|
|GET|GET请求对象|类似于字典的对象，GET的所有参数|
|POST|POST请求对象|类似于字典的对象，POST的所有参数|
|COOKIES|客户端cookies信息|字典类型|
|FILES|所有文件对象|字典类型，key是input标签中name的值|
|META|请求头信息|字典类型|
|get_host()|请求的原始主机|"127.0.0.1:8000"|
|get_full_path()|包含路径和查询字符串的路径|"/music/?print=true"|
|build_absolute_uri|绝对的url地址| "https://example.com/music/?print=true"|

## URL（项目目录下的urls.py）
- 代码示例
    ```
    from django.contrib import admin
    from django.urls import include, path
    
    urlpatterns = [
        path('app/', include('app.urls')),
        path('admin/', admin.site.urls),
    ]
    ```
- include() 允许引用其它 URL
-  path() 两个必须参数：route 和 view，两个可选参数：kwargs 和 name
   - route：是一个匹配 URL 的准则（类似正则表达式）。
   - view：url指定的视图函数，调用后传入一个 HttpRequest 对象作为第一个参数
   - kwargs：任意个关键字参数可以作为一个字典传递给目标视图函数。
   - name：为你的 URL 取名能使你在 Django 的任意地方唯一地引用它。
- path转换器
    - str：匹配任何非空字符串，但不含斜杠/，如果你没有专门指定转换器，那么这个是默认使用的；
    - int：匹配0和正整数，返回一个int类型
    - slug：可理解为注释、后缀、附属等概念，是url拖在最后的一部分解释性字符。该转换器匹配任何ASCII字符以及连接符和下划线，比如’ building-your-1st-django-site‘；
    - uuid：匹配一个uuid格式的对象。为了防止冲突，规定必须使用破折号，所有字母必须小写，例如’075194d3-6885-417e-a8a8-6c931e272f00‘ 。返回一个UUID对象；
    - path：匹配任何非空字符串，重点是可以包含路径分隔符’/‘。这个转换器可以帮助你匹配整个url而不是一段一段的url字符串。