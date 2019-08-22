from app.db import db


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(200), nullable=False)
    question = db.Column(db.Integer, db.ForeignKey('questions.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    author = db.relationship("User")

    def __init__(self, question, description=None):
        self.description = description
        self.question = question

    # Represent the object when it is queried
    def __repr__(self):
        return '<Answer: {}>'.format(self.description)

    def answer_as_dict(self):
        """Represent the question as a dict"""

        answer = {r.description: getattr(self, r.description)
                  for r in self.__table__.columns}
        answer['author'] = self.author.first_name + \
            ' ' + self.author.last_name
        return answer
