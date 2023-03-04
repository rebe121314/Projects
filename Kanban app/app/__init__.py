
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
#os allows me to use the path to the database
import os

# Initialize the Flask app
#find the project root directory to get the path to the database
project_dir = os.path.dirname(os.path.abspath(__file__))
# Create the database file in the project directory
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

# Create a SQLAlchemy object
db = SQLAlchemy(app)
# initialize the database
db.init_app(app)

# Import the database models
class Task(db.Model):
	__tablename__ = 'Task'
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	status = db.Column(db.String(50), nullable=False)


# Import routes
from app import routes




