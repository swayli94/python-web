# 导入 logging 模块并使用';'对其全局配置
# 'import logging; logging.basicConfig(level=logging.INFO)'也可以不使用';'写成两行：
# import logging
# logging.basicConfig(level=logging.INFO)
# logging 模块用法：参考自 https://zhuanlan.zhihu.com/p/56968001
# basicConfig 配置了 level 信息，level 配置为 INFO 信息，即只输出 INFO 级别的信息
# logging 日志的级别可参考下面的官方文档
# https://docs.python.org/zh-cn/3.8/library/logging.html?highlight=logging#logging-levels


import logging; logging.basicConfig(level=logging.INFO)

from aiohttp import web

'''
#*  logging



'''

#* Miao




# async 加不加都能跑，但是我们项目就是异步IO，后面可能要用
async def index(request):
    # 请求---》web---》响应（我是这么理解的，具体请看源码）
    # request         response
    return web.Response(body=b'<h1>Awesome</h1>',headers={'content-type':'text/html'})

def init():
    # 创建 web.Application ，这是我们web app的骨架
    app = web.Application()
    # 蔡老师源码如下：体会一下规范变了
    # app.router.add_route('GET', '/', index)
    app.router.add_get('/', index)
    # *** 在 Visual Studio Code 下你可以按住 'Ctrl' 键点击函数 查看源码！***
    # 尝试使用这个方法点击下面的 'run_app'
    # 下面这一行代码内部调用了 loop 和 logging （蔡老师的代码过时了）
    # 所以我们看似没调用开头导入的 logging 
    # 实际上你可以不导入 logging 试一下
    # 区别在于服务器终端会不会显示访问日志
    # 这是因为 aiohttp 的规范变了， aiohttp 官网在下面给出
    # http://demos.aiohttp.org/en/latest/tutorial.html
    web.run_app(app,host='127.0.0.1',port=9000)

    logging.info('server started at http://127.0.0.1:9000...')

    
if __name__ == '__main__':
    init()

'''

import asyncio


def index(request):
    return web.Response(body=b'<h1>Awesome</h1>')

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()



'''
