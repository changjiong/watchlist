import  os
import  sys

from flask import Flask, render_template
from flask import  url_for
from flask_sqlalchemy import  SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()

    return  render_template('index.html',  user=user, movies=movies)

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

import  click

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """ Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'Grey Li'
    movies =  [
    {'title': 'My Neighbor Totoro', 'year': '1987'},
    {'title': 'Dead Poets Society', 'year': '1988'},
    {'title': 'A Perfect World', 'year': '1992'},
    {'title': 'Leon', 'year': '1993'},
    {'title': 'Mahjong', 'year': '1995'},
    {'title': 'Swallowtail Butterfly', 'year': '1995'},
    {'title': 'King of Comedy', 'year': '1998'},
    {'title': 'Devils on the Doorstep', 'year': '1998'},
    {'title': 'WALL-E', 'year': '2007'},
    {'title': 'The Pork of Music', 'year': '2011'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

if __name__ == '__main__':
    app.run()
