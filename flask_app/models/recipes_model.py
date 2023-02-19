from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app import app
from flask import request, flash, session
from flask_app.models import users_model

#-----------------Clas constructor-------------------------------
class Recipes:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_cooked = data["date_cooked"]
        self.under_30 = data["under_30"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

#-----------------------Input into database-----------------

    @classmethod
    def input_recipe(cls,data):
        data = {
                **request.form,
                "owner_id": session["user_id"]
            }
            
        query="""INSERT INTO recipes (name, description, instructions, date_cooked, under_30, owner_id)
                    VALUES(%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30)s, %(owner_id)s)
            
            """
        return connectToMySQL(DATABASE).query_db(query, data)

#----------------------RETRIEVE ALL from database--------------------

    @classmethod
    def get_all_recipes(cls, data):
        
        query = """SELECT * from recipes
                    LEFT JOIN users ON recipes.owner_id = users.id
                    
        """

        return connectToMySQL(DATABASE).query_db(query, data)

#------------------RETRIVE ONE from database-------------------------------

    @classmethod
    def get_one_recipe(cls, data):
        
        query = """SELECT * from recipes
                    LEFT JOIN users ON recipes.owner_id = users.id
                    WHERE recipes.id = %(id)s
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        one_recipe = cls(results[0])

        
        result = results[0]
        data ={

            **result,
            "id" : result["users.id"],
            "created_at" : result["users.created_at"],
            "updated_at" : result["users.updated_at"]

        }
        
        one_recipe.owner = users_model.User(data)
        return one_recipe

#----------------UDPATE RECIPE in DATABASE------------------
    @classmethod
    def update_recipe_in_db(cls,data):
        query ="""
        UPDATE recipes SET name = %(name)s, description = %(description)s, 
        instructions = %(instructions)s, date_cooked = %(date_cooked)s, under_30 = %(under_30)s
        WHERE id = %(id)s
        """
        return connectToMySQL(DATABASE).query_db(query, data)

#-------------------DELETE RECIPE in DATABASE-----------------------------
    @classmethod
    def delete_old_recipe(cls,id):
        data = {
            "id" : id
        }
        query="DELETE FROM recipes WHERE id = %(id)s"

        return connectToMySQL(DATABASE).query_db(query, data)

#---------------Validate-------------------------------------------
    @staticmethod
    def validate(data):
        is_valid=True

        if len(data['name']) == 0:
            flash("Name required!")
            is_valid = False

        elif len(data['name']) < 3:
            flash("Name too short!")
            is_valid = False

        if len(data["description"]) == 0:
            flash("Description required!")
            is_valid = False

        elif len(data["description"]) < 3:
            flash("Description too short!")
            is_valid = False

        if len(data["instructions"]) == 0:
            flash("Instructions required!")
            is_valid = False
        
        elif len(data["instructions"]) < 3:
            flash("Instructions too short!")
            is_valid = False

        if "under_30" not in data:
            flash("Under 30 minutes required")
            is_valid = False

        if not data["date_cooked"]:
            flash("Date made required")
            is_valid = False

        return is_valid
        
        
