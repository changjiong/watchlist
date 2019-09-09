from flask import Flask
from flask import  url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def hello_world():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return  'user page: %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello_world'))
    print(url_for('user_page', name='greyli'))
    print(url_for('user_page', name='petterhome'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return  'Test Page'
if __name__ == '__main__':
    app.run()
