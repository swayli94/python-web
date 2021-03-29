
import time
import asyncio

'''
含有 yield 的函数 F()，成为一个生成器 f=F()
>>> def F():
>>>     while True:
>>>         res = yield 1

1.  yield 表现为 return
    当调用 next(f) 时，返回 yield 的结果 1，f 函数中断
    再次调用 next(f) 时，从中断处继续运行，res = None, 直至下一个 yield
    result = next(f) 等价于 result = f.__next__()

2.  对 yield 赋值
    当调用 f.send(0) 时，从中断处继续运行，res 被赋值为 0, 直至下一个 yield
'''

def producer(c):
    for i in range(3):
        print('Producer makes %d'%(i))
        c.send(str(i))

def consumer():
    while True:
        res = yield
        print('Consumer takes', res)

'''
同步：  线性地、序列地执行一系列任务
异步：  当前任务遇到堵塞时，直接运行下一任务；
        通过状态、通知、回调来调用处理结果

异步IO协程 asyncio

    event_loop: 无限循环，当满足事件发生时，调用相应的协程函数
    coroutine:  协程对象 async def F()，一个可挂起的函数
    task:       任务，对协程及其各种状态的封装，是 future 的子类
                保存了协程运行后的状态，用于未来获取协程的结果
    future:     将来执行或尚未执行的任务的结果，与 task 没有本质区别
                状态：pending, running, done, cancelled
    await:      关键字，用于挂起阻塞的异步调用接口
                类似于生成器中的 yield，函数遇到 await 则将自身挂起
                直至其他协程也挂起或执行完毕，再继续执行

'''
now = lambda: time.time()

def sync_sleep():
    time.sleep(1)

async def async_sleep():
    asyncio.sleep(1)    # 用于模拟耗时的IO操作

async def async_return(x):
    print('  async', x)
    return x

def callback(future):
    print('Callback:', future.result())

async def async_await(ID: int, x: int):
    print('Start IO %d'%(ID))
    await asyncio.sleep(x)
    return 'IO-%d %d(s)'%(ID, x)


if __name__ == '__main__':


    #* yield
    c = consumer()
    next(c)
    producer(c)
    print()


    #* sync and async
    t0 = now()
    for i in range(3):
        sync_sleep()
    print('Time for sync: %.3f'%(now()-t0))

    t0 = now()
    loop = asyncio.get_event_loop()     # 创建事件循环
    for i in range(3):
        loop.run_until_complete(async_sleep())  # 将协程加入事件循环
    print('Time for async: %.3f'%(now()-t0))

    print()


    #* task
    t0 = now()
    task = asyncio.ensure_future(async_sleep())   # 创建任务
    for i in range(3):
        loop.run_until_complete(task)   # 将协程加入事件循环
    print('Time for async: %.3f'%(now()-t0))

    t0 = now()
    task = loop.create_task(async_sleep())    # 创建任务
    print(task)
    for i in range(3):
        loop.run_until_complete(task)   # 将协程加入事件循环
        print(task, i)
    print(task)
    print('Time for async: %.3f'%(now()-t0))

    print()


    #* Call back
    coroutine = async_return(3)
    loop = asyncio.get_event_loop()
    task = loop.create_task(coroutine)
    task.add_done_callback(callback)    # 给任务添加绑定函数
    loop.run_until_complete(task)


    #* future & result
    coroutine = async_return(3)
    loop = asyncio.get_event_loop()
    task = loop.create_task(coroutine)
    loop.run_until_complete(task)
    print('Callback:', task.result())   # 直接获取状态为finished的task的返回结果
    print()


    #* await
    t0 = now()
    coroutine = async_await(1, 3)
    loop = asyncio.get_event_loop()
    task = loop.create_task(coroutine)
    loop.run_until_complete(task)
    print('Task result:', task.result())
    print('Time: %.3f'%(now()-t0))
    print()


    #* 协程并发
    t0 = now()
    coroutine1 = async_await(1, 1)
    coroutine2 = async_await(2, 2)
    coroutine3 = async_await(3, 3)
    tasks = [asyncio.ensure_future(coroutine1),
            asyncio.ensure_future(coroutine2),
            asyncio.ensure_future(coroutine3)]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    for task in tasks:
        print('Task result:', task.result())
    print('Time: %.3f'%(now()-t0))
    print()


    #* 协程嵌套
    async def main1():
        # 创建多个协程对象
        coroutine1 = async_await(1, 1)
        coroutine2 = async_await(2, 2)
        coroutine3 = async_await(3, 3)
        # 封装任务列表
        tasks = [asyncio.ensure_future(coroutine1),
                asyncio.ensure_future(coroutine2),
                asyncio.ensure_future(coroutine3)]
        # 获取返回结果
        return await asyncio.wait(tasks)

    t0 = now()
    loop = asyncio.get_event_loop()
    dones, pendings = loop.run_until_complete(main1())
    for task in dones:
        print('Task result:', task.result())
    print('Time: %.3f'%(now()-t0))
    print()

    async def main2():
        # 创建多个协程对象
        coroutine1 = async_await(1, 1)
        coroutine2 = async_await(2, 2)
        coroutine3 = async_await(3, 3)
        # 封装任务列表
        tasks = [asyncio.ensure_future(coroutine1),
                asyncio.ensure_future(coroutine2),
                asyncio.ensure_future(coroutine3)]
        # 获取返回结果
        return await asyncio.gather(*tasks)

    t0 = now()
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main2())
    for result in results:
        print('Task result:', result)
    print('Time: %.3f'%(now()-t0))
    print()

    async def main3():
        # 创建多个协程对象
        coroutine1 = async_await(1, 1)
        coroutine2 = async_await(2, 2)
        coroutine3 = async_await(3, 3)
        # 封装任务列表
        tasks = [asyncio.ensure_future(coroutine1),
                asyncio.ensure_future(coroutine2),
                asyncio.ensure_future(coroutine3)]
        # 获取返回结果
        for task in asyncio.as_completed(tasks):
            result = await task
            print('Task result:', result)

    t0 = now()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main3())
    print('Time: %.3f'%(now()-t0))
    print()


    #* 协程停止
    t0 = now()
    coroutine1 = async_await(1, 1)
    coroutine2 = async_await(2, 2)
    coroutine3 = async_await(3, 3)
    tasks = [asyncio.ensure_future(coroutine1),
            asyncio.ensure_future(coroutine2),
            asyncio.ensure_future(coroutine3)]

    loop = asyncio.get_event_loop()

    try:
        print('Keyboard Interrupt: Ctrl+C')
        loop.run_until_complete(asyncio.wait(tasks))

    except KeyboardInterrupt as e:
        # 获取事件循环中的所有任务列表
        '''
        for task in asyncio.Task.all_tasks():
            print(task.cancel())    # 返回 True，表示取消成功
        '''
        print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
        loop.stop()
        loop.run_forever()          # 对应于 finally 中的 loop.close()
    finally:
        loop.close()

    print('Time: %.3f'%(now()-t0))
    print()
