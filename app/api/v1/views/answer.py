from flask import jsonify, make_response, request, session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flasgger import swag_from
from sqlalchemy.sql import text

from app.db import db
from app.models.answer import Answer
from app.api.v1.helpers import validate_inputs


# RequestParser and added arguments will know which fields to accept and how to validate those
answer_request_parser = RequestParser(bundle_errors=True)
answer_request_parser.add_argument(
    "description", type=str, required=True, help="Description must be a valid string")


class AnswerCollection(Resource):
    """Operate on a list of answers, to view and add them"""

    @swag_from('../docs/answer/post.yml')
    def post(self, question_id):
        """Register a answer"""

        args = answer_request_parser.parse_args()

        invalid_input = validate_inputs(args)
        if invalid_input:
            return make_response(jsonify({"message": "{} must be a string of maximum {} characters".format(invalid_input[2], invalid_input[1])}), 400)

        description = args.get("description", None)

        sql = text(
            "SELECT * FROM answers WHERE description='{}' LIMIT 1".format(description))
        answer = db.engine.execute(sql)
        answer_result = {'answer': [dict(it) for it in answer]}
        if not answer_result['answer']:
            sql = text("INSERT into answers (description, question, created_at) VALUES ('{}', {}, CURRENT_TIMESTAMP)".format(
                description, question_id))
            db.engine.execute(sql)

            return make_response(
                jsonify({"message": "Answer added"}), 201)

        return make_response(jsonify({"message": "Answer already exists"}), 409)


class AnswerResource(Resource):
    """Operate on a single Answer, to view, update and delete it"""

    @swag_from('../docs/answer/put.yml')
    def put(self, answer_id):
        """Updates a answer"""

        sql = text("SELECT * FROM answers WHERE id='{}'".format(answer_id))
        answer = db.engine.execute(sql)
        answer_result = {'answer': [dict(it) for it in answer]}
        if answer_result['answer']:
            args = answer_request_parser.parse_args()

            invalid_input = validate_inputs(args)
            if invalid_input:
                return make_response(jsonify({"message": "{} must be a string of maximum {} characters".format(invalid_input[2], invalid_input[1])}), 400)

            description = args.get("description", None)
            question = args.get("question", None)

            # to avoid duplicating a answer
            sql = text(
                "SELECT * FROM answers WHERE description='{}' LIMIT 1".format(description))
            answer = db.engine.execute(sql)
            answer_result = {'answer': [dict(it) for it in answer]}
            if not answer_result['answer'] or (answer_result['answer'] and (answer_result['answer']['id']== answer_id)):
                sql = text("UPDATE answers SET description='{}', question='{}', updated_at=CURRENT_TIMESTAMP WHERE id='{}'".format(
                    description, question, answer_id))
                db.engine.execute(sql)

                return make_response(jsonify({"message": "Answer updated"}), 200)

            return make_response(jsonify({"message": "Answer already exists"}), 409)

        return make_response(jsonify({"message": "Answer not found"}), 404)

    @swag_from('../docs/answer/delete.yml')
    def delete(self, answer_id):
        """Delete a answer"""

        sql = text("SELECT * FROM answers WHERE id='{}'".format(answer_id))
        answer = db.engine.execute(sql)
        answer_result = {'answer': [dict(it) for it in answer]}
        if answer_result['answer']:
            sql = text(
                "DELETE FROM answers WHERE id='{}'".format(answer_id))
            db.engine.execute(sql)

            return make_response(jsonify({"message": "Answer deleted"}), 200)

        return make_response(jsonify({"message": "Answer not found"}), 404)
