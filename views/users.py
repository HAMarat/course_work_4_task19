from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service


user_ns = Namespace('users')


@user_ns.route('/')
class UsersViews(Resource):
    def get(self):
        all_users = user_service.get_all()
        all_users_js = UserSchema(many=True).dump(all_users)
        return all_users_js, 200

    def post(self):
        user_data = request.json
        user_service.create(user_data)
        return "", 201


@user_ns.route('/<int:uid>')
class UserViuws(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        user_js = UserSchema().dump(user)
        return user_js, 200

    def put(self, uid):
        user_data = request.data
        if not user_data.get("id"):
            user_data["id"] = uid
        user_service(user_data)
        return "", 200

    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
