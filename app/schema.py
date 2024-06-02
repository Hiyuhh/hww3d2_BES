import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import Movie as MovieModel, db
from app.models import Genre as GenreModel

class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel

class Genre(SQLAlchemyObjectType):
    class Meta:
        model = GenreModel

class Query(graphene.ObjectType):
    genres = graphene.List(Genre)
    movies = graphene.List(Movie)
    movie = graphene.Field(Movie, id=graphene.Int())
    genre = graphene.Field(Genre, id=graphene.Int())
    search_movies_by_genre = graphene.List(Movie, genre=graphene.String())
    search_genre_by_movie = graphene.List(Movie, title=graphene.String())

    def resolve_movies(root, info):
        return db.session.execute(db.select(MovieModel)).scalars().all()
    
    def resolve_genres(root, info):
        return db.session.execute(db.select(GenreModel)).scalars().all()
    
    def resolve_movie(root, info, id):
        return db.session.get(MovieModel, id)
    
    def resolve_genre(root, info, id):
        return db.session.get(GenreModel, id)
    
    def resolve_search_movies_by_genre(root, info, genre):
        genre = db.session.get(GenreModel, genre)
        if not genre:
            raise ValueError(f"{genre} does not exist.")
        return genre.movies
    
    def resolve_search_genre_by_movie(root, info, title):
        movie = db.session.get(MovieModel, title)
        if not movie:
            raise ValueError(f"{title} does not exist.")
        return movie.genres
        
class AddGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, name):
        if not name or len(name) > 30:
            raise ValueError("Try again!")

        genre = GenreModel(name=name)
        db.session.add(genre)
        db.session.commit()
        return AddGenre(genre=genre)
            
class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(root, info, id, name):
        genre = db.session.get(GenreModel, id)  
        if not genre:
            raise ValueError("Genre not found!")
        if not name or len(name) > 30:
            raise ValueError("Try again!")
        
        genre.name = name
        db.session.commit()
        return UpdateGenre(genre=genre)
    
class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    message = graphene.String()

    def mutate(root, info, id):
        genre = db.session.get(GenreModel, id)         
        if not genre:
            return DeleteGenre(message="Genre not found!")
        else:
            db.session.delete(genre)
            db.session.commit()
            return DeleteGenre(message="You have successfully deleted the genre!")
        
class Mutation(graphene.ObjectType):
    add_genre = AddGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)