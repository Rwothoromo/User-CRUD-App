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
