from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Data(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    id= db.Column(db.String(20))
    gender=db.Column(db.String(1))
    age = db.Column(db.Integer)

    tank_practice = db.Column(db.String(10))
    
    tank_reason = db.Column(db.String(10))

    despair = db.Column(db.Integer)
    anxiety = db.Column(db.Integer)
    irritation = db.Column(db.Integer)
    rage = db.Column(db.Integer)
    shame = db.Column(db.Integer)
    guilt = db.Column(db.Integer)

    feedback = db.Column(db.String(600))

    agent = db.Column(db.String(10))
    power = db.Column(db.String(10))
    