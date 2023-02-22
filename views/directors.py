from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from utils import auth_required
from parser import page_parser

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    """
    Представление на основе класса DirectorsView для отображения всех режиссеров
    """
    @auth_required
    def get(self):
        filters = page_parser.parse_args()
        rs = director_service.get_all(filters)
        res = DirectorSchema(many=True).dump(rs)
        return res, 200


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    """
    Представление на основе класса DirectorView для отображения режиссера по id
    """
    def get(self, did):
        r = director_service.get_one(did)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @auth_required
    def put(self, did):
        """
        Представление на основе класса DirectorView для обновления режиссера по id
        """
        director_data = request.json
        if not director_data.get("id"):
            director_data["id"] = did
        director_service.update(director_data)
        return "", 200

    @auth_required
    def delete(self, did):
        """
        Представление на основе класса DirectorView для удаления режиссера по id
        """
        director = director_service.get_one(did)
        director_service.delete(director)
        return "", 204
