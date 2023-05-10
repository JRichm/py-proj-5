"""  ####  Server Imports  ####  """

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from jinja2 import  StrictUndefined
import crud

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


"""  ####   Flask Routes   ####  """

##     """  View homepage """    ##
@app.route('/')
def homepage():
    return render_template('homepage.html')

##      """   New User   """     ##
@app.route('/users', methods=['POST'])
def register_user():
    
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not crud.get_user_by_email(email):
        if not crud.get_user_by_username(username):
            new_user = crud.create_user(username, password, email)
            db.session.add(new_user)
            db.session.commit()
        else:
            flash(f'Username {username} already in use! Try again.')
    else:
        flash('Invalid Email! Try logging in or enter a different email address.')
        
    return redirect('/')
    
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
    movie = crud.get_movie_by_id(movie_id)
    return render_template('movie_details.html', movie=movie)


"""  ####  Server Methods ####  """

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
