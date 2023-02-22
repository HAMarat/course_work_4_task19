from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service
from utils import auth_required
from parser import page_parser

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        filters = page_parser.parse_args()
        genres = genre_service.get_all(filters)
        result = GenreSchema(many=True).dump(genres)
        return result, 200


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        r = genre_service.get_one(gid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @auth_required
    def put(self, gid):
        genre_data = request.json
        if not genre_data.get("id"):
            genre_data["id"] = gid
        genre_service.update(genre_data)
        return "", 200

    @auth_required
    def delete(self, gid):
        genre = genre_service.get_one(gid)
        genre_service.delete(genre)
        return "", 204
