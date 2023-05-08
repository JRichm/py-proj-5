""" Script for seeding databse. """

import os
import json
from random import choice, randint
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
    
model.db.session.add_all(movies_in_db)
model.db.session.commit()