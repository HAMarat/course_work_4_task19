from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from utils import auth_required, admin_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    """
    Представление на основе класса DirectorsView
    """
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    """
    Представление на основе класса DirectorView
    """
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        director_data = request.json
        if not director_data.get("id"):
            director_data["id"] = rid
        director_service.update(director_data)
        return "", 200

    @admin_required
    def delete(self, rid):
        director = director_service.get_one(rid)
        director_service.delete(director)
        return "", 204
