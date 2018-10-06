## Gevent-Greenlet学习

### 1、二者关系
> 在gevent中用到的主要模式是Greenlet, 它是以C扩展模块形式接入Python的轻量级协程。 Greenlet全部运行在主程序操作系统进程的内部，但它们被协作式地调度。
当一个greenlet遇到IO操作时，比如访问网络，就自动切换到其他的greenlet，等到IO操作完成，再在适当的时候切换回来继续执行。由于IO操作非常耗时，经常使程序处于等待状态，有了gevent为我们自动切换协程，就保证总有greenlet在运行，而不是等待IO。
**在任何时刻，只有一个协程在运行。**

### 2、Gevent
####1、gevent特点：

 - 基于libev的快速事件循环，Linux上面的是epoll机制
 - 基于greenlet的轻量级执行单元
 - API复用了Python标准库里的内容
 - 支持SSL的协作式sockets
 - 可通过线程池或c-ares实现DNS查询
 - 通过monkey patching功能来使得第三方模块变成协作式


----------


####2、代码示例
```
import random
import gevent

def task(pid):
    """
    Some non-deterministic task
    """
    gevent.sleep(random.randint(0,2)*0.001)
    print('Task %s done' % pid)

def synchronous():
    for i in range(1,10):
        task(i)

def asynchronous():
    threads = [gevent.spawn(task, i) for i in range(10)]
    gevent.joinall(threads)

print('Synchronous:')
synchronous()

print('Asynchronous:')
asynchronous()

print("结束")
```
>运行结果：
```
Synchronous:
Task 1 done
Task 2 done
Task 3 done
Task 4 done
Task 5 done
Task 6 done
Task 7 done
Task 8 done
Task 9 done
Asynchronous:
Task 2 done
Task 5 done
Task 8 done
Task 1 done
Task 0 done
Task 3 done
Task 6 done
Task 4 done
Task 7 done
Task 9 done
结束
```
>分析结果：

 1. 在同步的部分，所有的task都同步的执行， 结果当每个task在执行时主流程被阻塞(主流程的执行暂时停住)。
 2. 异步的部分是将task函数封装到Greenlet内部线程的gevent.spawn。 初始化的greenlet列表存放在数组threads中，此数组被传给gevent.joinall 函数
 3. 异步部分执行时阻塞当前流程，并执行所有给定的greenlet。执行流程只会在 所有greenlet执行完后才会继续向下走,最后执行：print("结束")。
 4. 此外同步运行时间大约是每次停顿时间之和而异步执行时间大约是它们当中的最大停顿时间，因此**在受限于网络或IO的函数中使用gevent，这些函数会被协作式的调度， gevent的真正能力会得到发挥**。

----------
####3、greenlet具有确定性。在相同配置相同输入的情况下，它们总是 会产生相同的输出
代码实例：
```
import time
from gevent.pool import Pool

def echo(i):
    time.sleep(0.001)
    return i

p = Pool(10)
run1 = [a for a in p.imap_unordered(echo, range(10))]
run2 = [a for a in p.imap_unordered(echo, range(10))]
run3 = [a for a in p.imap_unordered(echo, range(10))]
run4 = [a for a in p.imap_unordered(echo, range(10))]

print(run1 == run2 == run3 == run4)
```
输出结果
```
True
```
>注意:与如socket或文件等外部服务交互时,可能会因竞争条件而出现不确定性。<br>
注：并发线程/进程都依赖于某个共享资源同时都尝试去修改它的时候, 就会出现竞争条件<br>
避免方法：**始终避免所有全局的状态**
### 3、创建Greenlets
>常用模板代码:
```
import gevent
from gevent import Greenlet

def foo(message, n):
    """
    Each thread will be passed the message, and n arguments
    in its initialization.
    """
    gevent.sleep(n)
    print(message)

# Initialize a new Greenlet instance running the named function
# foo
thread1 = Greenlet.spawn(foo, "Hello", 1)

# Wrapper for creating and running a new Greenlet from the named
# function foo, with the passed arguments
thread2 = gevent.spawn(foo, "I live!", 2)

# Lambda expressions
thread3 = gevent.spawn(lambda x: (x+1), 2)

threads = [thread1, thread2, thread3]

# Block until all threads complete.
gevent.joinall(threads)
```
### 4、Greenlet状态
 - started -- Boolean, 指示此Greenlet是否已经启动
 - ready() -- Boolean, 指示此Greenlet是否已经停止
 - successful() -- Boolean, 指示此Greenlet是否已经停止而且没抛异常
 - value -- 任意值, 此Greenlet代码返回的值
 - exception -- 异常, 此Greenlet内抛出的未捕获异常
 注：Greenlet运行失败后可能未能成功抛出异常，不能停止运行，或消耗了太多的系统资源。

### 5、终止程序
>在主程序中监听SIGQUIT信号，在程序退出 调用gevent.shutdown。以防止当主程序(mainprogram)收到一个SIGQUIT信号时，不能成功做yield操作的Greenlet可能会令意外地挂起程序的执行。这导致了所谓的僵尸进程， 它需要在Python解释器之外被kill掉。
代码示例：
```
import gevent
import signal

def run_forever():
    gevent.sleep(1000)

if __name__ == '__main__':
    gevent.signal(signal.SIGQUIT, gevent.shutdown)
    thread = gevent.spawn(run_forever)
    thread.join()
```
###6、超时
>超时是一种对一块代码或一个Greenlet的运行时间的约束。
代码示例：
```
import gevent
from gevent import Timeout

seconds = 10

timeout = Timeout(seconds)
timeout.start()

def wait():
    gevent.sleep(10)

try:
    gevent.spawn(wait).join()
except Timeout:
    print('Could not complete')
```
### 猴子补丁
>monkey.patch_socket()这个命令是用来改变标准socket库的。
### Greenlet运行机制：
- python中执行环境中创建greenlet对象的时候，将会先调用green_new方法，接着调用green_init方法，构造出父级parent，这个parent指向当前线程的greenlet。所以每个线程包含一个独立的主greenlet和一个子greenlet树。不可能在属于不同线程的greenlet之间混合或切换。
- 当一个greenlet调用switch()方法，会发生greenlet之间的切换，在这种情况下，执行会跳转到调用switch()的greenlet，或者当greenlet挂掉时，执行会跳转到父greenlet。
- 如果greenlet的run()完成，则其返回值是发送给其父级的对象。 如果run()以异常终止，则异常将传播到其父级（除非它是greenlet.GreenletExit异常，在这种情况下异常对象被捕获并返回给父级）
### Gevent基本思想
- 当一个greenlet遇到IO操作时，比如访问网络，就自动切换到其他的greenlet，等到IO操作完成，再在适当的时候切换回来继续执行。由于IO操作非常耗时，经常使程序处于等待状态，有了gevent为我们自动切换协程，就保证总有greenlet在运行，而不是等待IO。


----------
##协程和线程
>### **全局解释器锁(GIL)**
1. GIL在多线程情况下，保护共享资源，为了不让多个线程同时操作共享资源，导致不可预期的结果而加上的锁，在一个线程操作共享资源时，其他线程请求该资源，只能等待GIL解锁
2. GIL只允许一个线程来控制Python解释器。这意味着在任何时间点只有一个线程可以处于执行状态，即使在具有多个CPU核心的多线程体系结构中，GIL也是一次只允许一个线程执行。对执行单线程程序无太大影响。对CPU绑定和多线程代码影响较大。
3. CPython解释器中，线程的想要执行CPU指令需要2个条件：
- (1)被操作系统调度出来【操作系统允许它占用CPU】
- (2)获取到GIL【CPython解释器允许它执行指令】
经常出现的情况是：已经满足条件1，却被条件2限制,因此无法有效利用多核。
**理解：** CPython解释器中，GIL要求同一时间点只能一个线程执行，导致无法利用多核实现并发执行。多线程中线程之间切换时做大量重复工作（保存现场，准备新环境等），进而降低总的执行效率。多线程处理IO密集型任务时，有良好表现；处理计算密集型任务效果较差，可以使用多进程。
>## **协程**
**协程**：是一个程序组件，一个线程中可以拥有多个协程，在一个拥有多个协程的线程执行时会阻塞父线程，当一个正在执行的协程遇到IO操作时可以自动切换到线程中的其他协程，在适当的时候再返回来接着执行，所以一个线程执行代码段（程序）的顺序会因协程来回调度而不同。因为协程都在一个线程中所以不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态，这样资源开销非常低，执行速度非常快。
**注**：协程不是被操作系统内核所管理，而完全是由程序所控制（也就是在用户态执行）。

## **python实现协程模块**
- Gevent+Greenlet
- **asyncio**是主要由@asyncio.coroutine加yield from实现协程
```
import asyncio

@asyncio.coroutine
def hello():
    print("Hello world!")
    # 异步调用asyncio.sleep(1):
    r = yield from asyncio.sleep(1)
    print("Hello again!")

# 获取EventLoop:
loop = asyncio.get_event_loop()
# 执行coroutine
loop.run_until_complete(hello())
loop.close()
```
- **async/await**是由async和await实现协程,相比上面的代码简介易读。
```
import threading
import asyncio

async def hello():
    print('Hello world! (%s)' % threading.currentThread())
    await asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())

loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
```

## 补充：
> 1、协程比较于线程的优点：

 - 协程极高的执行效率。因为子程序切换不是线程切换，而是由程序自身控制，因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显。
 - 不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。

----------
>2、greenlet不是一种真正的并发机制，而是在同一线程内，在不同函数的执行代码块之间切换，实施“你运行一会、我运行一会”，并且在进行切换时必须指定何时切换以及切换到哪


