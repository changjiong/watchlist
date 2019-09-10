import click
import app
from app import db, User, Movie


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
    movies = [
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
