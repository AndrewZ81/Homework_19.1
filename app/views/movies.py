import sqlite3

from flask import request
from flask_restx import Resource, Namespace

from app.create_db import db
from app.models import Movie
from app.schemes import MovieSchema

movies_ns = Namespace("movies")  # Создаём пространство имён для фильмов

# Создаём экземпляры классов сериализации
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route("/")  # Создаём маршрут выборки всех фильмов и добавления фильма
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        if director_id and genre_id:
            movies = db.session.query(Movie).filter(Movie.director_id == int(director_id),
                                                    Movie.genre_id == int(genre_id)).all()
            if movies:
                return movies_schema.dump(movies), 200
            else:
                return "Таких режиссёра и жанра не существует", 404
        elif director_id:
            movies = db.session.query(Movie).filter(Movie.director_id == int(director_id)).all()
            if movies:
                return movies_schema.dump(movies), 200
            else:
                return "Такого режиссёра не существует", 404
        elif genre_id:
            movies = db.session.query(Movie).filter(Movie.genre_id == int(genre_id)).all()
            if movies:
                return movies_schema.dump(movies), 200
            else:
                return "Такого жанра не существует", 404
        else:
            movies = db.session.query(Movie).all()
            return movies_schema.dump(movies), 200

    def post(self):
        post_data = request.json
        movie = Movie(**post_data)
        try:
            db.session.add(movie)
            db.session.commit()
        except sqlite3.OperationalError:
            db.session.rollback()
            return "Не удалось добавить фильм", 404
        else:
            return "Фильм добавлен", 201


@movies_ns.route("/<int:id>")  # Создаём маршрут выборки, изменения и удаления одного фильма
class MovieView(Resource):
    def get(self, id):
        movie = db.session.query(Movie).get(id)
        if movie:
            return movie_schema.dump(movie), 200
        else:
            return "Такого фильма не существует", 404

    def put(self, id):
        put_data = request.json
        movie = db.session.query(Movie).get(id)
        if movie:
            try:
                movie.title = put_data.get("title")
                movie.description = put_data.get("description")
                movie.trailer = put_data.get("trailer")
                movie.year = put_data.get("year")
                movie.rating = put_data.get("rating")
                movie.genre_id = put_data.get("genre_id")
                movie.director_id = put_data.get("director_id")
                db.session.add(movie)
                db.session.commit()
            except sqlite3.OperationalError:
                db.session.rollback()
                return "Не удалось изменить фильм", 404
            else:
                return "Фильм изменён", 200
        else:
            return "Такого фильма не существует", 404

    def delete(self, id):
        movie = db.session.query(Movie).get(id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return "Фильм удалён", 200
        else:
            return "Такого фильма не существует", 404
