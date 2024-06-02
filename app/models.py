from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class MovieGenre(Base):
    __tablename__ = 'movie_genres'
    movie_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    genre_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('genres.id'), primary_key=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<MovieGenre {self.movie_id} {self.genre_id}>'

class Movie(Base):
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255))
    director: Mapped[str] = mapped_column(db.String(255))
    year: Mapped[int] = mapped_column(db.Integer)
    genres = relationship('Genre', secondary='movie_genres', back_populates='movies')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Movie {self.title}>'
    
class Genre(Base):
    __tablename__ = 'genres'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255))
    movies: Mapped[List['Movie']] = db.relationship('Movie', secondary='movie_genres', back_populates='genres')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Genre {self.name}>'