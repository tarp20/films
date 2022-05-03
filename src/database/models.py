import uuid

from src import db

movies_actors = db.Table(
    'movies_actors',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'),
              primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('films.id'),
              primary_key=True),
)


class Film(db.Model):
    __tablename__ = 'films'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, index=True, nullable=False)
    uuid = db.Column(db.String(36), unique=True)
    description = db.Column(db.Text)
    distributed_by = db.Column(db.String(128), nullable=False)
    length = db.Column(db.Float)
    rating = db.Column(db.Float)
    actors = db.relationship('Actor', secondary=movies_actors, lazy='subquery',
                             backref=db.backref('films', lazy=True))

    def __init__(self, title, release_date, description, distributed_by, length,
                 rating, actors=None):
        self.title = title
        self.release_date = release_date
        self.uuid = str(uuid.uuid4())
        self.description = description
        self.distributed_by = distributed_by
        self.length = length
        self.rating = rating
        if not actors:
            self.actors = []
        else:
            self.actors = actors

    def __repr__(self):
        return f'Film({self.title}, {self.release_date}, {self.uuid}, ' \
               f'{self.distributed_by}, {self.rating})'


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    birthday = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Actor {self.name}'
