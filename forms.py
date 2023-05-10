from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from flask import session, flash, redirect, render_template
from model import connect_to_db, db 
import crud

class LoginForm(FlaskForm):
    
    username = StringField('username', [validators.InputRequired()])
    password = PasswordField('password', [validators.InputRequired()])
    
    def login_user(self):
        if self.validate_on_submit():
            
            # user input data
            username = self.username.data
            password = self.password.data
            
            # get user obj using username
            user = crud.get_user_by_username(username)
            
            # check if user exists and if password is correct
            if not user or user.user_password != password:
                flash('Incorrect password')
                return redirect('/')
            
            # store username in session to keep track of logged in user
            session['username'] = user.user_name
            flash('Successfully Logged In!')
            return redirect('/')
        
        # form has not been submitted or data was not valid
        print('\tSomething Wen\'t Wrong')
        return render_template('homepage.html')
    
class CreateAccoutForm(FlaskForm):
    
    username = StringField('username', [validators.InputRequired()])
    email = StringField('email', [validators.InputRequired()])
    password = PasswordField('password', [validators.InputRequired()])
    
    def create_user(self):
    
        # user input data
        username = self.username.data
        email = self.email.data
        password = self.password.data
        
        # create user if username or email arent already in db
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
        