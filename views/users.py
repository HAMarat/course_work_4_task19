import sqlalchemy
from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service
from utils import get_data_from_header


user_ns = Namespace('user')

#
# @user_ns.route('/')
# class UsersViews(Resource):
#     """
#     Представление на основе класса UsersViews
#     """
#     def get(self):
#         all_users = user_service.get_all()
#         for user in all_users:
#             user.password = 0
#
#         all_users_js = UserSchema(many=True).dump(all_users)
#         return all_users_js, 200


@user_ns.route('/')
class UserViews(Resource):
    """
    Представление на основе класса UsersView
    """
    def get(self):
        data = request.headers
        user_data = get_data_from_header(data)
        user = user_service.get_by_email(user_data.get('email'))
        user.password = 0

        user_js = UserSchema().dump(user)
        return user_js, 200

    def patch(self):
        user_data = request.json
        user_service.update(user_data)
        return user_data, 200


@user_ns.route('/password')
class UserPasswordViews(Resource):
    def put(self):
        """
        Метод для обновления пароля с проверкой предыдущего
        """
        passwords = request.json
        passwords_old = passwords.get('password_1')
        passwords_new = passwords.get('password_2')

        data = request.headers
        user_data = get_data_from_header(data)
        user = user_service.get_by_email(user_data.get('email'))
        print(user.password)
        print(passwords_old)

        if user_service.password_check(passwords_old, user.password):
            user.password = user_service.get_hash(passwords_new)
            user_service.update(user)
            return "Пароль обновлён", 200

        return "Пароль не обновлён", 401
