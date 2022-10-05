from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash 
from flask_app.models.team import Team
from flask_app.models.player import Player
from flask_app.models.user import User
from flask_bcrypt import Bcrypt





@app.route('/team_info') #this is showing all team info 
def team_info():
    all_teams = Team.get_all()
    print(all_teams, 'OOOOO')
    return render_template('teams.html', all_the_teams = all_teams)


# @app.route('/team/<int:id>') #this is to view one teams players
# def view_post(id):
#     data = { 
#         'id' : id
#     }
#     a_player = Player.get_one_with_team(data) #this doesn't need to be looped through bc it is a dictionary not a list.
#     all_players = Player.get_all_with_team() #looping through bc it is returning a list on the class method
#     print(all_players, '******')
#     return render_template('team_info.html', one_player = a_player,  all_the_players = all_players)



@app.route('/team/<int:id>') #this is to show one teams's info
def one_team(id):
    data = {
        'id': id
    }
    a_team = Team.get_team_players(data)
    return render_template('team_info.html', one_team = a_team)

# @app.route('/team/<int:id>') #this is to view one users posts
# def view_post(id):
#     data = { 
#         'id' : id
#     }
#     a_player = Player.get_one_with_team(data) #this doesn't need to be looped through bc it is a dictionary not a list.
#     all_players = Player.get_all_with_team() #looping through bc it is returning a list on the class method
#     print(all_players, '******')
#     return render_template('team_info.html', one_player = a_player, all_the_players = all_players )



@app.route('/add_team') #form to create team
def create_team():
    return render_template("create_team.html")

@app.route('/submit_team', methods = ['POST']) #this is to create a team
def submit_team():
    print(request.form)
    if not Team.validate_create_team(request.form): #validations
        return redirect('/add_team') 
    data = {
        'team_name' : request.form['team_name'],
        'head_coach' : request.form['head_coach'],
        'assistant_coach' : request.form['assistant_coach'],
        "user_id" : session['user_id'] #this is coming from login 
    }
    Team.create(data) 
    return redirect ('/team_info')


@app.route('/delete_team/<int:id>', methods = ["POST"]) #this is to delete player
def delete_team(id):
    data = {
        'id' : id
    }
    Team.delete_team(data)
    return redirect ('/team_info')