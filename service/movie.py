from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, mid):
        return self.dao.get_one(mid)

    def get_all(self, filters):
        page = filters.get('page')
        status = filters.get('status')
        per_page = filters.get('per_page')

        if status == 'new':
            movies = self.dao.sort_by_filter(page, per_page)
        else:
            movies = self.dao.get_all(page, per_page)
        return movies

    def create(self, movie_d):
        return self.dao.create(movie_d)

    def update(self, movie_d):
        self.dao.update(movie_d)
        return self.dao

    def delete(self, mid):
        self.dao.delete(mid)
