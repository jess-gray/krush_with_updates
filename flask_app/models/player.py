from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import team

from flask import flash

class Player:
    def __init__(self,data):
        self.id = data['id'] 
        self.player_first_name = data['player_first_name']
        self.player_last_name = data['player_last_name']
        self.jersey_number = data['jersey_number']
        self.player_position = data['player_position']
        self.highschool = data['highschool']
        self.college_commit = data['college_commit']
        self.created_at = data['created_at']
        self.udpated_at = data['updated_at']
        self.owner = None #this is to associate the other table


    @classmethod  #this is to show all players with one team 
    def get_all_with_team(cls):
        query = 'SELECT * FROM players JOIN teams ON players.team_id = team.id'
        results = connectToMySQL('krush_project').query_db(query)
        all_players = []
        for row in results:
            one_player = cls(row)
            team_data = {
                'id': row['users.id'],
                'team_name' :row['team_name'],
                'head_coach' :row['head_coach'],
                'assistant_coach':row['assistant_coach'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            team_obj = team.Team(team_data)
            one_player.owner = team_obj
            all_players.append(one_player)
        return all_players
    
    @classmethod
    def get_one_with_team(cls, data): #to get one user and one post
        query = 'SELECT * FROM players JOIN teams ON players.user_id = teams.id WHERE players.id = %(id)s;'
        results = connectToMySQL('krush_project').query_db(query, data)
        one_player = cls(results[0])
        user_data = {
                'id': results[0]['users.id'],
                'team_name' : results[0]['team_name'],
                'head_coach': results[0]['head_coach'],
                'assistant_coach': results[0]['assistant_coach'],
                'created_at' : results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
            }
        one_player.owner = team.Team(user_data)    
        print(results)
        return one_player
