from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import team

from flask import flash

class Player:
    def __init__(self,data):
        self.id = data['id'] 
        self.player_first_name = data['player_first_name']
        self.player_last_name = data['player_last_name']
        self.player_position = data['player_position']
        self.highschool = data['highschool']
        self.college_commit = data['college_commit']
        self.created_at = data['created_at']
        self.udpated_at = data['updated_at']
        self.owner = None #this is to associate the other table