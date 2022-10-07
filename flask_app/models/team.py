from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import player

from flask import flash
import re


class Team: 
    def __init__(self,data):
        self.id = data['id']
        self.team_name = data['team_name']
        self.head_coach = data['head_coach']
        self.assistant_coach = data['assistant_coach']
        self.created_at = data['created_at']
        self.udpated_at = data['updated_at']
        self.players = [] #this is to associate the players table 
        self.user = None #this is to associate with User 


    @classmethod #this is to show all the teams
    def get_all(cls):
        query = 'SELECT * FROM teams ORDER BY team_name ASC;'
        results = connectToMySQL('krush_project').query_db(query)
        print(results)
        all_teams = []
        for one_team in results:
            all_teams.append(cls(one_team))
        return all_teams
    
    @classmethod #this is to show all the players under one team
    def get_team_players(cls, data):
        query = 'SELECT * FROM teams LEFT JOIN players ON teams.id = players.team_id WHERE teams.id = %(id)s ORDER BY jersey_number ASC;'
        results = connectToMySQL('krush_project').query_db(query, data)
        print(results)
        one_team = cls(results[0])
        for one_player in results:
            data = {
                'id': one_player['players.id'],
                'player_first_name' : one_player['player_first_name'],
                'player_last_name' : one_player['player_last_name'],
                'jersey_number': one_player['jersey_number'],
                'player_position' : one_player['player_position'],
                'highschool' : one_player['highschool'],
                'college_commit' : one_player['college_commit'],
                'created_at' : one_player['players.created_at'],
                'updated_at' : one_player['players.updated_at'],
                'team_id' : one_player['team_id']
            }
            player_obj = player.Player(data)
            one_team.players.append(player_obj)
        return one_team

    @classmethod #this is actually adding a new team
    def create(cls, data):
        query = 'INSERT INTO teams (team_name, head_coach, assistant_coach, user_id) VALUES (%(team_name)s, %(head_coach)s, %(assistant_coach)s, %(user_id)s);'
        results = connectToMySQL('krush_project').query_db(query, data)
        print(results)
        return results

    @classmethod #this is to delete team
    def delete_team(cls, data):
        query = 'DELETE FROM teams WHERE id = %(id)s;'
        results = connectToMySQL('krush_project').query_db(query, data)
        print(results)
        return results



    @staticmethod #validations for creating team
    def validate_create_team(reqForm):
        is_valid = True
        if len(reqForm['team_name']) <3:
            flash ('Team name must be 3 characters!')
            is_valid = False
        if len(reqForm['head_coach']) <3:
            flash ('Head coach must be at least 3 characters!')
            is_valid = False
        if len(reqForm['assistant_coach']) <3:
            flash ('Assistant coach must be at least 3 characters!')
            is_valid = False
        return is_valid
    