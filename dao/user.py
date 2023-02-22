from dao.model.user import User


class UserDao:

    def __init__(self, session):
        self.session = session

    def get_by_email(self, email):
        user = self.session.query(User).filter(User.email == email).first()
        return user

    def get_all(self):
        return self.session.query(User).all()

    def create(self, data):
        user = User(**data)
        self.session.add(user)
        self.session.commit()

    def update(self, user_data):
        user = self.get_by_email(user_data.get('email'))
        user.name = user_data.get('name')
        user.surname = user_data.get('surname')
        user.favorite_genre = user_data.get('favorite_genre')
        self.session.add(user)
        self.session.commit()

    def update_password(self, user_data):
        user = self.get_by_email(user_data.get('email'))
        user.password = user_data.get('password')
        self.session.add(user)
        self.session.commit()
