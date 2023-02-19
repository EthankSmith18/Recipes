from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app import app
import re
from flask_app import EMAIL_REGEX
from flask import request, flash, session
from flask_bcrypt import Bcrypt    
from flask_app.models import recipes_model
bcrypt = Bcrypt(app)

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        

#-----------------Validates Registration Form----------------------------
    @staticmethod
    def validate_form(data):
        is_valid = True
    #----------------------Validates first name-------------------------------
        if len(request.form["first_name"]) == 0:
            flash("No first name submitted", "registration")
            is_valid = False
        elif len(request.form["first_name"]) < 2:
            flash("User first name must be at least two characters", "registration")
            is_valid = False
        elif not request.form["first_name"].isalpha():
            flash("First name must only contain characters", "registration")
            is_valid = False


    #---------------------Validates last name---------------------------------

        if len(request.form["last_name"]) == 0:
            flash("No last name submitted", "registration")
            is_valid = False
        elif len(request.form["last_name"]) < 2:
            flash("User last name must be at least two characters", "registration")
            is_valid = False
        elif not request.form["last_name"].isalpha():
            flash("Last name must only contain characters", "registration")
            is_valid = False

    #------------------------Validates E-mail------------------------------------
        if len(request.form["email"]) == 0:
            flash("No E-mail address submitted", "registration")
            is_valid = False        
        elif len(request.form["password"]) < 2:
            flash("Password must be at least eight characters", "registration")
            is_valid = False
        elif not EMAIL_REGEX.match(request.form['email']):
            flash("Invalid email address!", "registration")
            is_valid = False
    #--------------------------Validates Password-----------------------------------
        if len(request.form["password"]) == 0:
            flash("No password submitted", "registration")
            is_valid = False
        elif request.form["password"] != request.form["confirm_password"]:
            flash("Passwords do not match", "registration")
            is_valid = False
        elif not any(char.isdigit() for char in request.form["password"]):
            flash("Password should have at least one numeral", "registration")
            is_valid = False
        elif not any(char.isupper() for char in request.form["password"]):
            flash("Password should have at least one uppercase letter", "registration")
            is_valid = False
        elif not any(char.islower() for char in request.form["password"]):
            flash("Password should have at least one lowercase letter", "registration")
            is_valid = False
        return is_valid

    @classmethod
    def register(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """
        return connectToMySQL(DATABASE).query_db(query, data)

#--------------------Find user by E-mail for login-------------------------------
    @classmethod
    def find_user(cls, data):
        query ="""
            SELECT * from users WHERE email = %(email)s
        """
        results = connectToMySQL(DATABASE).query_db(query,data)

        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False

#-----------------------------Validates Login---------------------
    @classmethod
    def validate_login(cls,data):

        found_user = cls.find_user(data)
        
        if not found_user:
            flash("Login is invalid", "login")
            return False
        elif not bcrypt.check_password_hash(found_user.password, data['password']):
            flash("Login is invalid", "login")
            return False
        
        return found_user

#---------------------------Checks E-mail Duplication for registration---------
    @classmethod
    def unique_email(cls, data):
        is_valid = True
        query = "SELECT email FROM users WHERE email = %(email)s"

        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return is_valid
        elif data["email"] in results[0]["email"]:
            flash("Email already in use!", "registration")
            is_valid = False
        return is_valid


#--------------------Get user by ID-------------------------------
    @classmethod
    def create_current_user(cls):
        
        data ={
            "id": session["user_id"]
        }

        query ="""
            SELECT * from users WHERE id = %(id)s
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        # print(results)
        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False
