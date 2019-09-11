import time
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user

from watchlist import app, db
from watchlist.models import User, Movie, SayHello


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form['title']
        rate = request.form['rate']

        if not title or not rate  or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('index'))

        movie = Movie(title=title, rate=rate)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    paginate = Movie.query.order_by(Movie.rate.desc()).paginate(page, per_page, error_out=False)
    movies = paginate.items

    return render_template('index.html', paginate=paginate, movies=movies)


@app.route('/sayhello', methods=['GET', 'POST'])
def sayhello():
    if request.method == 'POST':
        username = request.form['name']
        content = request.form['body']
        datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        say = SayHello(username=username, content=content, datetime=datetime)
        db.session.add(say)
        db.session.commit()
        flash('Your message have been sent to the world!')
        return redirect(url_for('sayhello'))

    says = SayHello.query.order_by(SayHello.id.desc()).all()
    return render_template('sayhello.html', says=says)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        rate = request.form['rate']

        if not title or not rate  or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.rate = rate
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)



@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


