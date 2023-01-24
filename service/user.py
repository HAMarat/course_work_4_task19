import hashlib
import hmac

from dao.user import UserDao
from constants import PWD_HASH_ITERATIONS, PWD_HASH_SALT


class UserService:
    def __init__(self, dao: UserDao):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        password = data.get('password')
        if password:
            data['password'] = self.get_hash(data['password'])
        return self.dao.create(data)

    def update(self, data):
        return self.dao.update(data)

    def delete(self, uid):
        self.dao.delete(uid)

    def get_hash(self, password):
        """
        Функция для хеширования паролей
        """
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

    def password_check(self, password, password_hash):
        """
        Функция для сравнения паролей в виде хеша
        """
        return hmac.compare_digest(password_hash, self.get_hash(password))
