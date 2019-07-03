"""
We would like to create a database of questions and answers for use during interviews:

  Model a database that has a relationship for:
    a) Categories i.e OOP, Algorithms, Databases, Data Structures
    b) Questions that belong to a specific category
    c) Questions Have answers.

    Examples
          Question: What is the distinctive feature of a set in python?
          Category: Data Structures
          Answer: Uniqueness

          Q: What is the distinctive feature of a tuple in python?
          C: Data Structures
          A: Immutability

          Q: Which noSQL datastores are provided by AWS?
          C: Databases
          A: DynamoDB
"""

from app.db import db


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    # user_id = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def __init__(self, title, description=None):
        self.title = title
        self.description = description

        # self.category = category
        # self.answers = answers

    # Represent the object when it is queried
    def __repr__(self):
        return '<Question: {}\{}>'.format(self.title, self.description)



class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    # Represent the object when it is queried
    def __repr__(self):
        return '<Category: {}\{}>'.format(self.name, self.description)


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    # user_id = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def __init__(self, title, description=None):
        self.title = title
        self.description = description
        # self.question = question

    # Represent the object when it is queried
    def __repr__(self):
        return '<Question: {}\{}>'.format(self.title, self.description)
