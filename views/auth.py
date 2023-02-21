import calendar
import datetime

import jwt
import sqlalchemy
from flask import request, abort
from flask_restx import Resource, Namespace

from dao.model.user import User
from implemented import user_service
from setup_db import db
from constants import secret, algo

auth_ns = Namespace("auth")


@auth_ns.route("/register")
class AuthViews(Resource):
    def post(self):
        auth_data = request.json
        email_js = auth_data.get("email")
        password_js = auth_data.get("password")

        if None in [email_js, password_js]:
            return f'Need enter email and password'

        # Обработка исключения при попытке добавления записи с не уникальным primary key
        try:
            user_service.create(auth_data)
        except sqlalchemy.exc.IntegrityError as error:
            return f'{error}', 500


@auth_ns.route("/login")
class AuthViews(Resource):
    """
    Представление на основе класса AuthViews
    """
    def post(self):
        auth_data = request.json
        email_js = auth_data.get("email")
        password_js = auth_data.get("password")

        if None in [email_js, password_js]:
            abort(400)

        user = db.session.query(User).filter(User.email == email_js).first()

        if not user:
            abort(401)

        password_hash = user.password

        if not user_service.password_check(password_js, password_hash):
            abort(401)

        data = {
            "email": user.email
        }

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
        return tokens, 200

    def put(self):
        auth_data = request.json
        print(auth_data)
        refresh_token = auth_data.get('refresh_token')
        print(refresh_token)

        if not refresh_token:
            abort(401)

        try:
            data = jwt.decode(refresh_token, secret, algo)
        except Exception as e:
            return {e}

        email_js = data.get('email')

        user = db.session.query(User).filter(User.email == email_js).first()

        if not user:
            abort(400)

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
        return tokens, 200
