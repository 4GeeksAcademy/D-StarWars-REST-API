from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorites", back_populates= "user")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model): 
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="favorites")
    people = db.relationship("User", back_populates="favorites")
    planet = db.relationship("User", back_populates="favorites")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "people": self.people,
            "planet":self.planet
        }


class People(db.Model): 
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable = False)
    description = db.Column(db.String(200), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    
class Planets(db.Model): 
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable = False)
    description = db.Column(db.String(200), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    
    
