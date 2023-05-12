"""  ####  Server Imports  ####  """

from flask import Flask, render_template, request, flash, session, redirect, url_for
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
    logged_in = session.get('user_id') is not None
    return render_template('homepage.html', form=forms.LoginForm(), username=check_login())

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

##      """  User Logout """     ##
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))
    
##      """  View Users  """     ##
@app.route('/users', methods=['GET'])
def all_users():
    users = crud.get_users()
    return render_template('users.html', users=users, username=check_login())

##      """  View User   """     ##
@app.route('/users/<user_id>')
def show_user(user_id):
    user = crud.get_user_by_id(user_id)
    return render_template('user_details.html', user=user, username=check_login())

##      """  View Movies """     ##
@app.route('/movies')
def all_movies():
    movies = crud.get_movies()
    return render_template('movies.html', movies=movies, username=check_login())

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
                           form=forms.RateMovieForm(),
                           username=check_login())

##      """  Rate Movie  """     ##
@app.route('/rate-movie', methods=['POST'])
def rate_movie():    
    form = forms.RateMovieForm(request.form)
    if not session.get('user_id') is not None:
        flash('Please login to rate movies!', 'danger')
        return redirect(f'/movies/{session.get("movie_id")}')
    else:
        return form.add_rating(session['movie_id'], session.get('user_id'))


"""  ####  Server Methods ####  """

def check_login():
    if session.get('user_id') is not None:
        return crud.get_user_by_id(session['user_id']).user_name
    return None       
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
