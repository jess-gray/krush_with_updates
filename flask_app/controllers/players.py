from flask_app import app
from flask import Flask, render_template, request, redirect, session
from flask_app.models.team import Team
from flask_app.models.player import Player
from flask_app.models.user import User


@app.route('/add_player') #form to create player
def create_player():
    all_teams = Team.get_all()
    return render_template("create_player.html", all_the_teams = all_teams)

@app.route('/submit_player', methods = ['POST']) #this is to create a player
def submit_player():
    print(request.form)
    if not Player.validate_create_player(request.form): #validations
        return redirect('/add_player') 
    data = {
        'player_first_name' : request.form['player_first_name'],
        'player_last_name' : request.form['player_last_name'],
        'jersey_number' : request.form['jersey_number'],
        'player_position' : request.form['player_position'],
        'highschool' : request.form['highschool'],
        'college_commit' : request.form['college_commit'],
        'team_id' : request.form['team_id'],
        "user_id" : session['user_id'] #this is coming from login 
    }
    Player.create_player(data) 
    return redirect (f'team/{request.form["team_id"]}')

@app.route('/delete/<int:id>', methods = ["POST"]) #this is to delete player
def delete(id):
    data = {
        'id' : id
    }
    Player.delete(data)
    return redirect ('/team_info')



@app.route('/edit/<int:id>') #this is the edit page/form
def edit(id):
    data = { #this is pulling show id
        'id' : id
    }
    a_player = Player.get_one_with_team(data)
    return render_template('edit_player.html', one_player = a_player)


@app.route('/submit_player/<int:id>', methods = ['POST']) #this is to actually edit the user
def update(id):
    if not Player.validate_edit_player(request.form): #validations
        return redirect(f'/edit/{id}') 
    data = {
        'id' : id,
        'player_first_name' : request.form['player_first_name'],
        'player_last_name' : request.form['player_last_name'],
        'jersey_number' : request.form['jersey_number'],
        'player_position' : request.form['player_position'],
        'highschool' : request.form['highschool'],
        'college_commit' : request.form['college_commit']
    }
    Player.update(data)
    return redirect('/team_info')


    