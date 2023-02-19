from flask import Flask
app = Flask(__name__)
import re
app.secret_key = "shhhhhh"
DATABASE = 'recipes_db'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
