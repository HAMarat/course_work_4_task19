from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service
from utils import get_data_from_header
from utils import auth_required

user_ns = Namespace('user')


@user_ns.route('/')
class UserViews(Resource):
    """
    Представление на основе класса UsersView
    """
    @auth_required
    def get(self):
        """
        Метод для возвращения данных о пользователе
        """
        data = request.headers
        user_data = get_data_from_header(data)
        user = user_service.get_by_email(user_data.get('email'))
        user.password = 0

        user_js = UserSchema().dump(user)
        return user_js, 200

    @auth_required
    def patch(self):
        user_data = request.json
        user_service.update(user_data)
        return user_data, 200


@user_ns.route('/password')
class UserPasswordViews(Resource):
    @auth_required
    def put(self):
        """
        Метод для обновления пароля с проверкой предыдущего
        """
        passwords = request.json
        passwords_old = passwords.get('password_1')
        passwords_new = passwords.get('password_2')

        # получаем данные пользователя из базы по 'email' полученному из токена в headers
        data = request.headers
        user_data = get_data_from_header(data)
        user = user_service.get_by_email(user_data.get('email'))

        # перед обновлением пароля, проверяем старый
        if user_service.password_check(passwords_old, user.password):
            user.password = '0'
            user_js = UserSchema().dump(user)
            user_service.update_password(user_js, passwords_new)
            return "Пароль обновлён", 200

        return "Пароль не обновлён", 401
