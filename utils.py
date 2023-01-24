import jwt
from flask import request, abort

from constants import secret, algo


def auth_required(func):
    """
    Декоратор для проверки авторизации пользователя
    """
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, secret, algo)

        except Exception as e:
            print(f"{e}")
            abort(401)
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    """
    Декоратор для ограничения доступа только для пользователей с правами администратора
    """
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            user = jwt.decode(token, secret, algo)
            role = user.get('role')
        except Exception as e:
            print(f"{e}")
            abort(401)

        if role != "admin":
            abort(403)
        return func(*args, **kwargs)
    return wrapper
