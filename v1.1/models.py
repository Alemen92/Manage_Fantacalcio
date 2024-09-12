
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    total_budget = db.Column(db.Integer, nullable=False)
    remaining_budget = db.Column(db.Integer, nullable=False)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    team = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
