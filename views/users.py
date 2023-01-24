import sqlalchemy
from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service


user_ns = Namespace('users')


@user_ns.route('/')
class UsersViews(Resource):
    """
    Представление на основе класса UsersViews
    """
    def get(self):
        all_users = user_service.get_all()
        for user in all_users:
            user.password = 0

        all_users_js = UserSchema(many=True).dump(all_users)
        return all_users_js, 200

    def post(self):
        user_data = request.json
        # Обработка исключения при попытке добавления записи с не уникальным primary key
        try:
            user_service.create(user_data)
        except sqlalchemy.exc.IntegrityError as error:
            return f'{error}', 500


@user_ns.route('/<int:uid>')
class UserViews(Resource):
    """
    Представление на основе класса UsersView
    """
    def get(self, uid):
        user = user_service.get_one(uid)
        user_js = UserSchema().dump(user)
        if user_js:
            return user_js, 200
        return f"Пользователя с id {uid} не найден", 404

    def put(self, uid):
        user_data = request.json
        if "id" not in user_data:
            user_data["id"] = uid
        user_service.update(user_data)
        return "", 200

    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
