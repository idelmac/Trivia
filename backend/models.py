import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from marshmallow import Schema, fields,validate
from flask_migrate import Migrate

database_name = 'trivia'
database_path = 'postgresql://{}:{}@{}/{}'.format(
    'postgres','12345678','localhost:5432', database_name)

db = SQLAlchemy()
#migrate = Migrate()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['JSON_SORT_KEYS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)

"""
Question

"""
class QuestionSchema(Schema):
    question = fields.String(required=True,allow_none=False,validate=validate.Length(min=1))
    answer = fields.String(required=True,allow_none=False,validate=validate.Length(min=1))
    category = fields.Integer(required=True,allow_none=False,validate=validate.Range(min=1))
    difficulty = fields.Integer(required=True,allow_none=False,validate=validate.Range(min=1))
    #rating = fields.Integer(required=True,allow_none=False,validate=validate.Range(min=1))

class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(Integer)
    difficulty = Column(Integer)
    #rating = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
        #self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
            }

"""
Category

"""
class CategorySchema(Schema):
    type = fields.String(required=True,allow_none=False,validate=validate.Length(min=1))

class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # def format(self):
    #     return {
    #         'id': self.id,
    #         'type': self.type
    #         }
    
    # def format(self):
    #     return {
    #         self.id: self.type
    #         }
        
    # def __repr__(self):
    #   return f'<id:{self.id}, type:{self.type}>'
