from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import player

from flask import flash
import re


class Team: 
    def __init__(self,data):
        self.id = data['id']
        self.team_name = ['team_name']
        self.head_coach = ['head_coach']
        self.assistant_coach = ['assistant_coach']
        self.created_at = data['created_at']
        self.udpated_at = data['updated_at']
        self.players = [] #this is to associate the other table