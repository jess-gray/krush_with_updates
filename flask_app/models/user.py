from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import player

from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User: 
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.reg_code = data['reg_code']
        self.created_at = data['created_at']
        self.udpated_at = data['updated_at']


    @classmethod #this is actually adding the new user
    def create(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, reg_code, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(reg_code)s, %(password)s);'
        results = connectToMySQL('krush_project').query_db(query, data)
        print(results)
        return results
    
    @classmethod #this is to get user info by email 
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('krush_project').query_db(query, data)
        print(results)
        if results == (): #this is to help validate the email address is not in db
            return False
        return cls(results[0])
    

    #validations 

    @staticmethod #this is validating a new user registering 
    def validate_create(reqForm):
        is_valid = True
        if len(reqForm['first_name']) < 2:
            flash('User first name is too short!')
            is_valid = False
        if len(reqForm['last_name']) < 2:
            flash('User last name is too short!')
            is_valid = False
        if not EMAIL_REGEX.match(reqForm['email']): #make sure import re/REGEX is added for this to work 
            flash('Invalid email address')
            is_valid = False
        data = {
            'email' : reqForm['email']
        }
        user_in_db = User.get_by_email(data) #this is to check to see if email is already in database
        if user_in_db:
            flash('Email already registered')
            is_valid = False
        if len(reqForm['password']) < 8:
            flash('Password is too short!')
            is_valid = False
        elif (reqForm['password']) != (reqForm['password_confirm']): #this is to confirm passwords are the same. password_confirm came from HTML form
            flash('Passwords do not match!')
            is_valid = False
        if (reqForm['reg_code']) != 'VBALL':
            flash('Must have valid registration code for login access')
            is_valid = False
        return is_valid