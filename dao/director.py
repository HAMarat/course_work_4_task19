from dao.model.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Director).get(bid)

    def get_all(self, page):
        return self.session.query(Director).paginate(page=page, per_page=12)

    def create(self, director_d):
        ent = Director(**director_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def update(self, director_d):
        director = self.get_one(director_d.get("id"))
        director.name = director_d.get("name")

        self.session.add(director)
        self.session.commit()
