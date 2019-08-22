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
    author = db.relationship("User")

    def __init__(self, category, description=None):
        self.description = description
        self.category = category

    # Represent the object when it is queried
    def __repr__(self):
        return '<Question: {}>'.format(self.description)

    def question_as_dict(self):
        """Represent the question as a dict"""

        question = {r.name: getattr(self, r.name)
                    for r in self.__table__.columns}
        question['author'] = self.author.first_name + \
            ' ' + self.author.last_name
        return question
