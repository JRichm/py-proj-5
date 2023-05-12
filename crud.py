"""  ####  CRUD Functions  ####  """

from model import db, User, Movie, Rating, connect_to_db

""" #    Contructor Methods    # """
def create_movie(title, description, release_date, poster_path):
    movie = Movie(
        movie_title = title,
        movie_description = description,
        movie_release_date = release_date,
        movie_poster_path = poster_path
    )
    return movie

def create_user(username, password, email):
    user = User(
        user_name=username,
        user_password=password,
        user_email=email
    )
    return user
    
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

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email):
    return User.query.filter(User.user_email == email).first()

def get_user_by_username(username):
    return User.query.filter(User.user_name == username).first()


  # ratings
def get_movie_ratings(movie_id):
    all_ratings = Rating.query.filter(Rating.rating_movie_id==movie_id).all()
    return all_ratings

def get_movie_avg_rating(movie_id):
    all_ratings = Rating.query.filter(Rating.rating_movie_id==movie_id).all()
    ratings = [0, 0]
    for rating in all_ratings:
        ratings[0] = ratings[0] + 1
        ratings[1] = ratings[1] + rating.rating_score
    
    if not ratings[0] == 0:
        ratings = str(round(ratings[1] / ratings[0], 1))
    else:
        ratings = 'No Data'
    return ratings

def get_rating(movie_id, user_id):
    user_rating = Rating.query.filter(Rating.rating_movie_id==movie_id).filter(Rating.rating_user_id==user_id).first()
    if user_rating:
        return user_rating  
    else:
        return None

""" #      Server Methods       # """
if __name__ == '__main__':
    from server import app
    connect_to_db(app)