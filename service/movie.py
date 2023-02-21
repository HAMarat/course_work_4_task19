from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self, filters):
        page = filters.get('page')
        status = filters.get('status')

        if status == 'new':
            movies = self.dao.sort_by_filter()
        else:
            movies = self.dao.get_all()
        return movies.paginate(page=page, per_page=12)

    def create(self, movie_d):
        return self.dao.create(movie_d)

    def update(self, movie_d):
        self.dao.update(movie_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)
