from app.db import db


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    answers = db.relationship('Answer', order_by='Answer.id')

    def __init__(self, category, description=None):
        self.description = description
        self.category = category

    # Represent the object when it is queried
    def __repr__(self):
        return '<Question: {}>'.format(self.description)
