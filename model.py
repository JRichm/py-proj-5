"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(), unique=True, nullable=False)
    user_password = db.Column(db.String(), nullable=False)
    user_email = db.Column(db.String(), nullable=True)
    
    # user.ratings variable available through 'Rating' backref
    # ratings = a list of Rating objects 
    
    def __repr__(self):
        return f'<User Data:\n\t{self.user_name} ({self.user_id})\n\t{self.user_email}>'
        
class Rating(db.Model):
    __tablename__ = 'ratings'
    
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating_score = db.Column(db.Integer, nullable=False)
    rating_movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    rating_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    movie = db.relationship('Movie', backref='ratings')
    user = db.relationship('User', backref='ratings')
    
    def __repr__(self):
        return f'<Rating Data\n\tRating ID: {self.rating_id}\n\tMovie ID: {self.rating_movie_id}\n\tScore: {self.rating_score}\n\tUser: {self.rating_user_id}>'

class Movie(db.Model):
    __tablename__ = 'movies'
    
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_title = db.Column(db.String(), nullable=False)
    movie_description = db.Column(db.Text(), nullable=True)
    movie_release_date = db.Column(db.DateTime(), nullable=False)
    movie_poster_path = db.Column(db.String(), nullable=False)
    
    # movie.ratings variable available through 'Rating' backref
    # ratings = a list of Rating objects 
    
    def __repr__(self):
        return f'<Movie Data\n\t{self.movie_title} ({self.movie_id})\n\t{self.movie_description}\n\t{self.movie_release_date}>'


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
