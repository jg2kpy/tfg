import json

class Movies_info():
    def __init__(self, fromJson=None):
        self.movies_info = []
        if isinstance(fromJson, str):
            try:
                movies = json.loads(fromJson)
                self.movies_info = [
                    Movie_info(fromJson=movie) for movie in movies
                ]
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string provided")
        elif fromJson is not None:
            raise TypeError("fromJson must be a string containing valid JSON or None")

    def to_json(self):
        return json.dumps([movie.to_json() for movie in self.movies_info])

    def get_movie_by_id(self, movie_id):
        for movie in self.movies_info:
            if movie.movie_id == movie_id:
                return movie
        return None

    def get_or_create_movie_by_id(self, movie_id):
        for movie in self.movies_info:
            if movie.movie_id == movie_id:
                return movie
        movie = Movie_info(movie_id)
        return movie

    def add_movie(self, new_movie_info):
        self.movies_info.append(new_movie_info)

    def get_len_movies(self):
        return len(self.movies_info)

    def get_all_movies(self):
        return self.movies_info

    def get_all_movies_content(self):
        return {movie.movie_id: movie.content for movie in self.movies_info if movie.content is not None}

    def get_all_movie_ids(self):
        return [movie.movie_id for movie in self.movies_info]

    def get_profit_by_movie_id(self, movie_id):
        for movie in self.movies_info:
            if movie.movie_id == movie_id:
                return movie.profit
        return None

    def get_all_newcomers(self):
        all_newcomers = []
        for movie in self.movies_info:
            if movie.is_newcomer:
                all_newcomers.append(movie)
        return all_newcomers

    def get_all_newcomers_ids(self):
        all_newcomers_ids = []
        for movie in self.movies_info:
            if movie.is_newcomer:
                all_newcomers_ids.append(movie.movie_id)
        return all_newcomers_ids

    def get_movies_with_profits(self):
        return {movie.movie_id: movie.profit for movie in self.movies_info if movie.profit is not None}

    def get_movies_popularity(self):
        return {movie.movie_id: movie.popularity for movie in self.movies_info if movie.popularity is not None}

    def get_movies_id_sort_by_popularity(self):
        return [movie.movie_id for movie in sorted(self.movies_info, key=lambda x: x.popularity, reverse=True)]


class Movie_info():
    def __init__(self, movie_id=None, profit=None, is_newcomer=None, popularity = None, fromJson=None):
        if fromJson:
            self.movie_id = fromJson['movie_id']
            self.profit = fromJson['profit']
            self.is_newcomer = fromJson['is_newcomer']
            self.popularity = fromJson.get('popularity', 0)
            self.content = fromJson['content']
        else:
            self.movie_id = movie_id
            self.profit = profit
            self.is_newcomer = is_newcomer
            self.popularity = popularity
            self.content = None

    def get_id(self):
        return self.movie_id

    def set_content(self, content):
        self.content = content

    def get_content(self):
        return self.content

    def to_json(self):
        return {
            'movie_id': self.movie_id,
            'profit': self.profit,
            'is_newcomer': self.is_newcomer,
            'popularity': self.popularity,
            'content': self.content
        }
