from config import Config
from app import create_app
from setup_db import db

if __name__ == '__main__':
    with create_app(Config()).app_context():
        db.drop_all()
        db.create_all()
