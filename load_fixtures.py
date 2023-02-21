from contextlib import suppress
from typing import Any, Dict, List, Type

from sqlalchemy.exc import IntegrityError

from config import Config
from dao.model.genre import Genre
from dao.model.movie import Movie
from dao.model.director import Director
from app import create_app
from setup_db import db
from utils import read_json


def load_data(data, model) -> None:
    for item in data:
        item['id'] = item.pop('pk')
        db.session.add(model(**item))


if __name__ == '__main__':
    fixtures = read_json("fixtures.json")

    with create_app(Config()).app_context():
        load_data(fixtures['movies'], Movie)
        load_data(fixtures['genres'], Genre)
        load_data(fixtures['directors'], Director)

        with suppress(IntegrityError):
            db.session.commit()
