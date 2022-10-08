from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash, jsonify 
import requests 
from flask_app.models.user import User
from flask_app.models.player import Player
from flask_app.models.team import Team 


from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/login')
def user_login():
    return render_template('login.html')

@app.route('/register_user', methods = ['POST']) #this is to actually register a user
def register_user():
    print(request.form) #print statement should be on all post methods to make sure the information is being taken in 
    if not User.validate_create(request.form): #validation needs to happen BEFORE hashing 
        return redirect('/login')
    pw_hash = bcrypt.generate_password_hash(request.form['password']) #hashing - make sure Bcrpyt is installed/imported 
    print(pw_hash)    
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'reg_code' : request.form['reg_code'],
        'password' : pw_hash
    }
    user_id = User.create(data)
    session['user_id'] = user_id #this key is IMPORTANT to hold information (Result of an insert query)
    return redirect('/team_info')

@app.route('/login_user', methods = ['POST']) #this is to login a user
def login():
    print(request.form)
    data = {
        "email" : request.form['email']
        }
    user_in_db = User.get_by_email(data)
    if not user_in_db: #checks to see if email is correct
        flash('Invalid Email/password')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']): #checks to see if password is correct
        flash('Invalid Email/password')
        return redirect('/login')
    session['user_id'] = user_in_db.id #this is result of select query 
    return redirect('/team_info')

@app.route('/logout') #this is to logout
def logout():
    session.clear() #this clears the session 
    return redirect('/krushvbc')


@app.route('/krushvbc') #this is the homepage
def route():
    if "user_id" not in session:     #can I do this backwards?
        return render_template('index.html')
    data = {
        'id' : session['user_id']
    }
    return render_template('index.html', active_user = User.get_by_id(data))

# @app.route('/map_data')
# def getMapdata():
#     headers = {
#     'X-RapidAPI-Key': MAP_API_KEY,
#     'X-RapidAPI-Host': "trueway-directions2.p.rapidapi.com"
#     }
#     r = requests.get(f'FindDrivingRoute?stops=40.629041%2C-74.025606%3B40.630099%2C-73.993521%3B40.644895%2C-74.013818%3B40.627177%2C-73.980853", headers=headers')
#     return jsonify(r.json())
