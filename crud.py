"""  ####  CRUD Functions  ####  """

from model import db, User, Movie, Rating, connect_to_db

""" #    Contructor Methods    # """

def create_user(username, password, email):
    user = User(
        user_name=username,
        user_password=password,
        user_email=email
    )
    return user

def create_movie(title, description, release_date, poster_path):
    movie = Movie(
        movie_title = title,
        movie_description = description,
        movie_release_date = release_date,
        movie_poster_path = poster_path
    )
    return movie
    
def create_rating(user, movie, score):
    rating = Rating(rating_score=score, rating_movie_id=movie, rating_user_id=user)
    return rating


""" #        Get Methods        # """

  # movies
def get_movies():
    return Movie.query.all()

def get_movie_by_id(movie_id):
    return Movie.query.get(movie_id)

  # users
def get_users():
    return User.query.all()

def get_user_by_id(movie_id):
    return User.query.get(movie_id)

if __name__ == '__main__':
    from server import app
    connect_to_db(app)