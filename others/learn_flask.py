
from flask import Flask, render_template

#* 创建web应用程序
app = Flask(__name__)

#* 处理浏览器发送的请求
@app.route('/')         # 当访问 127.0.0.1:5000/ 时运行的函数
def index():
    return render_template('home_page.html')    # 默认搜索 template/ 中的文件

@app.route('/meow')     # 当访问 127.0.0.1:5000/meow 时运行的函数
def meow():
    return 'Hello meow'

#* 处理传入可变变量
@app.route('/string')
def pass_string():
    s = 'New string'
    return render_template('string.html', s=s)

@app.route('/list')
def pass_list():
    s = 'Passing a list'
    l = ['String', 1, 1.0]
    return render_template('list.html', s=s, l=l)


if __name__ == '__main__':

    app.run()






