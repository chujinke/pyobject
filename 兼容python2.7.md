# 兼容python2.7

## encoding声明
- python默认使用ascii编码去解释源文件。
- 如果源文件中出现了非ASCII码字符，不在开头声明encoding会报错。
- 可以声明为utf8，告诉解释器用utf8去读取文件代码，这个时候源文件有中文也不会报错。
- 兼容python2.7需要在每个python文件头部加上编码声明,这样程序就能在python2.7上正常运行。
- python3.6默认编码是utf8，所以修改后不影响程序正常执行。
```
# encoding=utf8
print '中文'
```

## python2.7中的str和unicode

- python2.7中的字符串一般有两种类型，unicode和str。
- str为字节码，会根据某种编码把字符串转成一个个字节，这个时候字符和字节没有所谓固定的一一对应的关系。
- unicode则是用unicode编码的字符串，一个字符是对应两个字节的。
- 直接赋值字符串，类型为str，str为字节串，会按照开头的encoding来编码成一个个的字节。
- 赋值的时候在字符串前面加个u，类型则为unicode，直接按照unicode来编码。
- 用到的地方是豆瓣标签页判断标签是否是‘英国 喜剧 2015’,在字符串前加个u,不影响python3.6版本。
```
verification_tag =  u"英国 喜剧 2015"
```

## 测试案例
- python2.7下测试过程遇到的问题是test.py文件中包含中文的子程序无法正常执行，修改test.py后python3.6版本下无法正常执行
- 解决方案是在出错子程序中判断python版本，进而执行不同程序，使得在不同版本下都能正常运行。





