from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.recipes_model import Recipes
from flask_app.models.users_model import User

@app.route("/new")
def new_recipe():
    if not "user_id" in session:
        flash("ACCESS DENIED. User not logged in.", "session")  
        return redirect("/")
    return render_template("new.html")
#--------------------------------CREATE RECIPE ROUTE---------------------
@app.route("/create", methods=["POST"])
def create_recipe():

    if not Recipes.validate(request.form):
        return redirect("/new")

    Recipes.input_recipe(request.form)
    
    return redirect("/welcome")
#--------------------------------------SHOW EDIT ROUTE----------------------------------------
@app.route("/show_edit/<int:id>")
def show_edit_recipe(id):
        
    data={
        "id":id
    }

    recipe = Recipes.get_one_recipe(data).recipes[0]

    if not "user_id" in session:
        flash("ACCESS DENIED. User not logged in.", "session")  
        return redirect("/")

    return render_template("edit.html", recipe=recipe)

#------------------------------UPDATE RECIPE ROUTE----------------------------------------------
@app.route("/update", methods=["POST"])
def update_recipe():

    if not Recipes.validate(request.form):
        return redirect("/show_edit/" + request.form["id"])

    Recipes.update_recipe_in_db(request.form)

    return redirect("/welcome")
#-------------------------------------SHOW RECIPES ROUTE-------------------------------
@app.route("/recipes/<int:id>")
def show_recipe(id):
    if not "user_id" in session:
        flash("ACCESS DENIED. User not logged in.", "session")  
        return redirect("/")

    data={
        "id":id
    }
    recipe = Recipes.get_one_recipe(data)
    current_user = User.create_current_user()
    
    return render_template ("recipes.html", recipe=recipe, user = current_user)

#-----------------------DELETE RECIPE ROUTE---------------------------
@app.route("/delete/<int:id>")
def delete_recipe(id):
    if not "user_id" in session:
        flash("ACCESS DENIED. User not logged in.", "session")  
        return redirect("/")

    Recipes.delete_old_recipe(id)

    return redirect("/welcome")



