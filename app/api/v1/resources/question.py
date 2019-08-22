from flask import jsonify, make_response, request, session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flasgger import swag_from
from sqlalchemy.sql import text

from app.db import db
from app.models.question import Question
from app.api.v1.resources.helpers import validate_inputs


# RequestParser and added arguments will know which fields to accept and how to validate those
question_request_parser = RequestParser(bundle_errors=True)
question_request_parser.add_argument(
    "description", type=str, required=True, help="Description must be a valid string")


class QuestionCollection(Resource):
    """Operate on a list of questions, to view and add them"""

    @swag_from('docs/question/get_all.yml')
    def get(self):
        """Retrieves all questions"""

        sql = text("SELECT * FROM questions ORDER BY description ASC")

        questions = db.engine.execute(sql)
        questions_result = {'questions': [
            dict(question) for question in questions]}
        if not questions_result['questions']:
            return make_response(jsonify({"message": "No question found"}), 404)

        return make_response(jsonify(questions_result), 200)

    @swag_from('docs/question/post.yml')
    def post(self):
        """Register a question"""

        args = question_request_parser.parse_args()

        invalid_input = validate_inputs(args)
        if invalid_input:
            return make_response(jsonify({"message": "{} must be a string of maximum {} characters".format(invalid_input[2], invalid_input[1])}), 400)

        description = args.get("description", None)
        category = args.get("category", None)

        sql = text(
            "SELECT * FROM questions WHERE description='{}' LIMIT 1".format(description))
        question = db.engine.execute(sql)
        question_result = {'question': [dict(it) for it in question]}
        if not question_result['question']:
            category_sql = text(
                "SELECT * FROM categories WHERE name='{}' LIMIT 1".format(category))
            category_query = db.engine.execute(category_sql)
            category_result = {'category': [dict(it) for it in category_query]}
            if not category_result['category']:
                category_sql = text(
                    "INSERT into categories (name) VALUES ('{}')".format(category))

            sql = text("INSERT into questions (description, category) VALUES ('{}', '{}')".format(
                description, category))
            db.engine.execute(sql)

            return make_response(
                jsonify({"message": "Question added"}), 201)

        return make_response(jsonify({"message": "Question already exists"}), 409)


class QuestionResource(Resource):
    """Operate on a single Question, to view, update and delete it"""

    @swag_from('docs/question/get.yml')
    def get(self, question_id):
        """Get a question"""

        sql = text("SELECT * FROM questions WHERE id='{}'".format(question_id))
        question = db.engine.execute(sql)
        question_result = {'question': [dict(it) for it in question]}
        if question_result['question']:
            return make_response(jsonify(dict(question_result)), 200)

        return make_response(jsonify({"message": "Question not found"}), 404)

    @swag_from('docs/question/put.yml')
    def put(self, question_id):
        """Updates a question"""

        sql = text("SELECT * FROM questions WHERE id='{}'".format(question_id))
        question = db.engine.execute(sql)
        question_result = {'question': [dict(it) for it in question]}
        if question_result['question']:
            args = question_request_parser.parse_args()

            invalid_input = validate_inputs(args)
            if invalid_input:
                return make_response(jsonify({"message": "{} must be a string of maximum {} characters".format(invalid_input[2], invalid_input[1])}), 400)

            description = args.get("description", None)
            category = args.get("category", None)

            # to avoid duplicating a question
            sql = text(
                "SELECT * FROM questions WHERE description='{}' LIMIT 1".format(description))
            question = db.engine.execute(sql)
            question_result = {'question': [dict(it) for it in question]}
            if not question_result['question'] or (question_result['question'] and (question_result['question'].id == question_id)):

                category_sql = text(
                    "SELECT * FROM categories WHERE name='{}' LIMIT 1".format(category))
                category_query = db.engine.execute(category_sql)
                category_result = {'category': [dict(it) for it in category_query]}
                if not category_result['category']:
                    category_sql = text(
                        "INSERT into categories (name) VALUES ('{}')".format(category))

                sql = text("UPDATE questions SET description='{}', category='{}' WHERE id='{}'".format(
                    description, category, question_id))
                db.engine.execute(sql)

                return make_response(jsonify({"message": "Question updated"}), 200)

            return make_response(jsonify({"message": "Question already exists"}), 409)

        return make_response(jsonify({"message": "Question not found"}), 404)

    @swag_from('docs/question/delete.yml')
    def delete(self, question_id):
        """Delete a question"""

        sql = text("SELECT * FROM questions WHERE id='{}'".format(question_id))
        question = db.engine.execute(sql)
        question_result = {'question': [dict(it) for it in question]}
        if question_result['question']:
            sql = text(
                "DELETE FROM questions WHERE id='{}'".format(question_id))
            db.engine.execute(sql)

            return make_response(jsonify({"message": "Question deleted"}), 200)

        return make_response(jsonify({"message": "Question not found"}), 404)
