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


@app.route('/team/<int:id>') #this is to view one teams players
def view_post(id):
    data = { 
        'id' : id
    }
    a_player = Player.get_one_with_team(data) #this doesn't need to be looped through bc it is a dictionary not a list.
    all_players = Player.get_all_with_team() #looping through bc it is returning a list on the class method
    print(all_players, '******')
    return render_template('read_one.html', one_player = a_player,  all_the_players = all_players)

    #Need to add link on teams html and create view one team html. Also need to add a player to test it is working 