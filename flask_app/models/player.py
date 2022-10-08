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
        self.owner = None #this is to associate with team
        self.user = None #to associate with user


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
    def get_one_with_team(cls, data): #to get one player and team
        query = 'SELECT * FROM players JOIN teams ON players.team_id = teams.id WHERE players.id = %(id)s;'
        results = connectToMySQL('krush_project').query_db(query, data)
        one_player = cls(results[0])
        user_data = {
                'id': results[0]['teams.id'],
                'team_name' : results[0]['team_name'],
                'head_coach': results[0]['head_coach'],
                'assistant_coach': results[0]['assistant_coach'],
                'created_at' : results[0]['teams.created_at'],
                'updated_at' : results[0]['teams.updated_at']
            }
        one_player.owner = team.Team(user_data)    
        print(results)
        return one_player
    
    @classmethod
    def create_player(cls, data): #to create a new player
        query = 'INSERT INTO players (player_first_name, player_last_name, jersey_number, player_position, highschool, college_commit, team_id, user_id) VALUES (%(player_first_name)s, %(player_last_name)s, %(jersey_number)s, %(player_position)s, %(highschool)s, %(college_commit)s, %(team_id)s, %(user_id)s);'
        results = connectToMySQL('krush_project').query_db(query, data)
        print(results)
        return results

    @classmethod #this is to delete player
    def delete(cls, data):
        query = 'DELETE FROM players WHERE id = %(id)s;'
        results = connectToMySQL('krush_project').query_db(query, data)
        print(results)
        return results

    @classmethod #this is to actually edit the player
    def update(cls, data):
        query = 'UPDATE players set player_first_name = %(player_first_name)s, player_last_name = %(player_last_name)s, jersey_number = %(jersey_number)s, player_position = %(player_position)s, highschool = %(highschool)s, college_commit = %(college_commit)s WHERE id = %(id)s;'
        results = connectToMySQL('krush_project').query_db(query, data)
        print(results)
        return results
    
    @classmethod #this is to get user info by jersey # # need to join on team 
    def get_by_number(cls, data):
        query = 'SELECT * FROM players WHERE jersey_number = %(jersey_number)s;'
        results = connectToMySQL('krush_project').query_db(query, data)
        print(results)
        if results == (): #this is to help validate the jersey # is not in db
            return False
        return cls(results[0])

#want to add validation to check jersey number against database 
# Need to fix function so it takes from a specific team

    @staticmethod #validations for creating team   
    def validate_create_player(reqForm):
        is_valid = True
        print("XX:" + reqForm['jersey_number'])
        if len(reqForm['player_first_name']) <3:
            flash ('first name must be 3 characters!')
            is_valid = False
        if len(reqForm['player_last_name']) <3:
            flash ('last name must be at least 3 characters!')
            is_valid = False
        if reqForm['jersey_number'] == "" or int(reqForm['jersey_number']) <1 :
            flash ('must enter jesrsey number!')
            is_valid = False
        # data = {
        #     'jersey_number' : reqForm['jersey_number']
        # }
        # jersey_in_db = Player.get_by_number(data)        
        # if jersey_in_db:
        #     flash('jersey number already taken!')
        #     is_valid = False
        if len(reqForm['highschool']) <3:
            flash ('high school must be at least 3 characters!')
            is_valid = False
        return is_valid

    @staticmethod #validations for editing team
    def validate_edit_player(reqForm):
        is_valid = True
        if len(reqForm['player_first_name']) <3:
            flash ('first name must be 3 characters!')
            is_valid = False
        if len(reqForm['player_last_name']) <3:
            flash ('last name must be at least 3 characters!')
            is_valid = False
        if reqForm['jersey_number'] == "" or int(reqForm['jersey_number']) <1 :
            flash ('must enter jesrsey number!')
            is_valid = False
        if len(reqForm['highschool']) <3:
            flash ('high school must be at least 3 characters!')
            is_valid = False
        return is_valid
    
    