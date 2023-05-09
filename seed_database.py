""" Script for seeding databse. """

import os
import json
import string
import random
from datetime import datetime

import crud
import model
import server

os.system('dropdb -U jamcam ratings')
os.system('createdb -U jamcam ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())
    
movies_in_db = []
for each in movie_data:
    title, overview, poster_path = (
        each['title'],
        each['overview'],
        each['poster_path']
    )
    release_date = datetime.strptime(each['release_date'], '%Y-%m-%d')
    
    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)
    
    
def random_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

users_in_db = []
for each in range(10):
    username = random_string(8)
    password = random_string(10)
    email = f'{username}@{random_string(4)}.com'
    
    db_fake_user = crud.create_user(username, password, email)
    users_in_db.append(db_fake_user)
    model.db.session.add(db_fake_user)
    
    users_ratings = []
    for rating in range(10):
        movie_to_rate = random.choice(movies_in_db)
        score = random.randint(1, 5)
        
        rating = crud.create_rating(len(users_in_db), random.randint(1,80), score)
        model.db.session.add(rating)
        
    
model.db.session.add_all(movies_in_db)
model.db.session.commit()