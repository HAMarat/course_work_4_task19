from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from implemented import movie_service
from utils import auth_required
from parser import page_parser

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        """
        Метод для отображения всех фильмов с возможностью отображения
        по страницам с выбором количества отображаемых фильмов на странице
        """
        filters = page_parser.parse_args()
        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    @auth_required
    def post(self):

        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid):
        movie = movie_service.get_one(mid)
        sm_d = MovieSchema().dump(movie)
        return sm_d, 200

    @auth_required
    def put(self, mid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = mid
        movie_service.update(req_json)
        return "", 204

    @auth_required
    def delete(self, mid):
        movie_service.delete(mid)
        return "", 204
