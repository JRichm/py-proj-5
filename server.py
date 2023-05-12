"""  ####  Server Imports  ####  """

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from jinja2 import  StrictUndefined
import crud
import forms

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


"""  ####   Flask Routes   ####  """
##     """  View homepage """    ##
@app.route('/')
def homepage():
    return render_template('homepage.html', form=forms.LoginForm())

##      """   New User   """     ##
@app.route('/users', methods=['POST'])
def register_user():
    form = forms.CreateAccoutForm(request.form)
    return form.create_user()

##      """  User Login  """     ##
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm(request.form)
    return form.login_user()
    
##      """  View Users  """     ##
@app.route('/users', methods=['GET'])
def all_users():
    users = crud.get_users()
    return render_template('users.html', users=users)

##      """  View User   """     ##
@app.route('/users/<user_id>')
def show_user(user_id):
    user = crud.get_user_by_id(user_id)
    return render_template('user_details.html', user=user)

##      """  View Movies """     ##
@app.route('/movies')
def all_movies():
    movies = crud.get_movies()
    return render_template('movies.html', movies=movies)

##      """  View Movie  """     ##
@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    session['movie_id'] = movie_id
    movie = crud.get_movie_by_id(movie_id)
    movieRatings = crud.get_movie_ratings(movie_id)
    movieAvgRating = crud.get_movie_avg_rating(movie_id)
    return render_template('movie_details.html',
                           movie=movie,
                           movieRatings=movieRatings,
                           movieAvgRating=movieAvgRating,
                           form=forms.RateMovieForm())

##      """  Rate Movie  """     ##
@app.route('/rate-movie', methods=['POST'])
def rate_movie():
    
    print('\nThis is my user_id:')
    print(session['user_id'])
    
    form = forms.RateMovieForm(request.form)
    return form.add_rating(session['movie_id'], session['user_id'])


"""  ####  Server Methods ####  """

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
