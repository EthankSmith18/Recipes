from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)
from flask_app.models.users_model import User
from flask_app.models.recipes_model import Recipes 

#-----------------Route to main page-------------------------------
@app.route("/")
def main():
    return render_template("index.html")

#---Route that validates Registration fields, checks for email dup, hashes password, registers user-----------------------
@app.route("/registration", methods=["POST"])
def registration_validaton():

    if not User.validate_form(request.form):
        return redirect('/')
    
    if not User.unique_email(request.form):
        return redirect("/")

    hash = bcrypt.generate_password_hash(request.form["password"])
    

    data = {
        **request.form,
        "password" : hash
    }
    
    
    user_login = User.register(data)
    
    return redirect("/")

#----Check login credentials, creates user session, displays welcome page or redirects to login page--------
@app.route("/login", methods=["POST"])
def login():

    user_login = User.validate_login(request.form)
    if not user_login:
        return redirect("/")
    session['user_id'] = user_login.id
    

    data ={
            "id": user_login.id
        }
    
    user_recipes = Recipes.get_all_recipes(data)
    # print(user_recipes)
    return redirect("/welcome")

#------Checks to see if user in session before accessing welcome page-------------------------
@app.route("/welcome")
def welcome():


    if not "user_id" in session:
        flash("ACCESS DENIED. User not logged in.", "session")  
        return redirect("/")
    data ={
            "id": session["user_id"]
        }
    
    user_recipes = Recipes.get_all_recipes(data)
    
    current_user = User.create_current_user()

    return render_template("welcome.html", user=current_user, recipes = user_recipes)

#------Clears user from session------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")