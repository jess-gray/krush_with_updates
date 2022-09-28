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


    @classmethod #this is to show all the teams
    def get_all(cls):
        query = 'SELECT * FROM teams;'
        results = connectToMySQL('krush_project').query_db(query)
        print(results)
        all_teams = []
        for one_team in results:
            all_teams.append(cls(one_team))
        return all_teams