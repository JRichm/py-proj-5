#####   #  Server Imports  #   #####
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from jinja2 import  StrictUndefined
import crud

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

#####   #   Flask Routes   #   #####
##      """ View homepage """     ##
@app.route('/')
def homepage():
    return render_template('homepage.html')


##      """  View Users  """     ##
@app.route('/users')
def all_users():
    return render_template('users.html')

##      """  View Movies """     ##
@app.route('/movies')
def all_movies():
    movies = crud.get_movies()
    return render_template('movies.html', movies=movies)

##      """  View Movie  """     ##
@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template('movie_details.html', movie=movie)


#####   #  Server Methods  #   #####
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
