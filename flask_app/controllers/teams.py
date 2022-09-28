from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash 
from flask_app.models.team import Team
from flask_app.models.player import Player
from flask_app.models.user import User
from flask_bcrypt import Bcrypt



@app.route('/krushvbc') #this is the homepage
def route():
    return render_template('index.html')

@app.route('/team_info') #this is showing all team info 
def team_info():
    all_teams = Team.get_all()
    print(all_teams, 'OOOOO')
    return render_template('teams.html', all_the_teams = all_teams)