import calendar
import datetime

import jwt
from flask import request, abort
import json

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


def read_json(filename: str, encoding: str = "utf-8") -> list | dict:
    with open(filename, encoding=encoding) as f:
        return json.load(f)


def get_tokens(data):
    """
    Функция для создания токенов
    """
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data['exp'] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, secret, algo)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data['wxp'] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, secret, algo)

    tokens = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    return tokens


def get_data_from_header(request_header):
    """
    Функция для получения данных из headers
    """
    if 'Authorization' not in request_header:
        abort(401)

    data = request.headers['Authorization']
    token = data.split("Bearer ")[-1]
    try:
        user = jwt.decode(token, secret, algo)
    except Exception as e:
        print(f"{e}")
        abort(401)
    return user
