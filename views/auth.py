import calendar
import datetime

import jwt
from flask import request, abort
from flask_restx import Resource, Namespace

from dao.model.user import User
from implemented import user_service
from setup_db import db
from constants import secret, algo

auth_ns = Namespace("auth")


@auth_ns.route("/")
class AuthViews(Resource):
    """
    Представление на основе класса AuthViews
    """
    def post(self):
        auth_data = request.json
        username_js = auth_data.get("username")
        password_js = auth_data.get("password")
        role_js = auth_data.get("role")

        if None in [username_js, password_js]:
            abort(400)

        user = db.session.query(User).filter(User.username == username_js, User.role == role_js).first()

        if not user:
            abort(401)

        password_hash = user.password

        if not user_service.password_check(password_js, password_hash):
            abort(401)

        data = {
            "username": user.username,
            "role": user.role
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
        refresh_token = auth_data.get('refresh_token')

        if not refresh_token:
            abort(401)

        try:
            data = jwt.decode(refresh_token, secret, algo)
        except Exception as e:
            return {e}

        username_js = data.get('username')

        user = db.session.query(User).filter(User.username == username_js).first()

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
