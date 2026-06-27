import json

class Users():
    def __init__(self, fromJson=None):
        self.users = []
        if isinstance(fromJson, str):
            try:
                users = json.loads(fromJson)
                self.users = [
                    User(fromJson=movie) for movie in users
                ]
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string provided")
        elif fromJson is not None:
            raise TypeError("fromJson must be a string containing valid JSON or None")

    def to_json(self):
        return json.dumps([user.to_json() for user in self.users])

    def add_user(self, new_user):
        self.users.append(new_user)

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def get_or_create_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        user = User(user_id)
        self.users.append(user)
        return user

    def get_all_users(self):
        return self.users

    def get_len_users(self):
        return len(self.users)

    def get_movies_and_ratings_by_user_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return [(movie, rating) for movie, rating in zip(user.movies, user.ratings)]
        return None

    def set_users(self, new_users):
        self.users = new_users

    def delete_movie(self, movie_id):
        count = 0
        for user in self.users:
            if user.delete_movie(movie_id):
                count+=1
                if user.get_len_movie() == 0:
                    self.users.remove(user)
        return count

    def get_user_movie_ratings(self):
        user_movie_ratings = {}
        for user in self.users:
            for movie, rating in zip(user.movies, user.ratings):
                user_movie_ratings[(user.user_id, movie)] = rating
        return user_movie_ratings

    def get_all_users_profile(self):
        return {user.user_id: user.get_profile() for user in self.users if user.get_profile() is not None}

class User():
    def __init__(self, user_id=None, fromJson=None):
        if fromJson:
            self.user_id = fromJson['user_id']
            self.movies = fromJson['movies']
            self.ratings = fromJson['ratings']
            self.profile = fromJson['profile']
        else:
            self.user_id = user_id
            self.movies = []
            self.ratings = []
            self.profile = None

    def to_json(self):
        return {
            'user_id': self.user_id,
            'movies': self.movies,
            'ratings': self.ratings,
            'profile': self.profile
        }

    def get_id(self):
        return self.user_id

    def add_movie_rating(self, new_movie_id, new_rating):
        self.movies.append(new_movie_id)
        self.ratings.append(new_rating)

    def get_movie_ids(self):
        return self.movies

    def get_ratings(self):
        return self.ratings

    def get_rating_by_movie_id(self, movie_id):
        position = self.movies.index(movie_id)
        return self.ratings[position]

    def get_movies_and_ratings(self):
        return list(zip(self.movies, self.ratings))

    def delete_movie(self, movie_id):
        if movie_id in self.movies:
            position = self.movies.index(movie_id)
            self.ratings.pop(position)
            self.movies.pop(position)
            return True
        return False

    def get_len_movie(self):
        return len(self.movies)

    def set_profile(self, profile):
        self.profile = profile

    def get_profile(self):
        return self.profile
