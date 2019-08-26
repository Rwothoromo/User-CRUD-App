from flask import jsonify, make_response, request, session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flasgger import swag_from
from sqlalchemy.sql import text

from app.db import db
from app.models.user import User
from app.api.v1.helpers import validate_inputs


# RequestParser and added arguments will know which fields to accept and how to validate those
user_request_parser = RequestParser(bundle_errors=True)
user_request_parser.add_argument(
    "first_name", type=str, required=True, help="First name must be a valid string")
user_request_parser.add_argument(
    "last_name", type=str, required=True, help="Last name must be a valid string")
user_request_parser.add_argument(
    "username", type=str, required=True, help="Username must be a valid string")


# for search by name q
q_request_parser = RequestParser(bundle_errors=True)
q_request_parser.add_argument(
    "q", type=str, required=False, help="Search user by name")


# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class UserCollection(Resource):
    """Operate on a list of users, to view and add them"""

    @swag_from('../docs/user/get_all.yml')
    def get(self):
        """Retrieves all users"""

        args = q_request_parser.parse_args()
        q = args.get('q', None)

        if q:
            q = q.lower()
            sql = text(
                "SELECT * FROM users WHERE LOWER(first_name) like '%{}%' OR LOWER(last_name) like '%{}%' OR LOWER(username) like '%{}%'".format(q, q, q))
        else:
            sql = text("SELECT * FROM users ORDER BY first_name ASC")

        users = db.engine.execute(sql)
        users_result = {'users': [dict(user) for user in users]}
        if not users_result['users']:
            return make_response(jsonify({"message": "No user found"}), 404)

        return make_response(jsonify(users_result), 200)

    @swag_from('../docs/user/post.yml')
    def post(self):
        """Register a user"""

        args = user_request_parser.parse_args()

        invalid_input = validate_inputs(args)
        if invalid_input:
            return make_response(jsonify({"message": "{} must be a string of maximum {} characters".format(invalid_input[2], invalid_input[1])}), 400)

        first_name = args.get("first_name", None)
        last_name = args.get("last_name", None)
        username = args.get("username", None)

        sql = text(
            "SELECT * FROM users WHERE username='{}' LIMIT 1".format(username))
        user = db.engine.execute(sql)
        user_result = {'user': [dict(it) for it in user]}
        if not user_result['user']:
            sql = text("INSERT into users (first_name, last_name, username, created_at) VALUES ('{}', '{}', '{}', CURRENT_TIMESTAMP)".format(
                first_name, last_name, username))
            db.engine.execute(sql)

            return make_response(
                jsonify({"message": "User added"}), 201)

        return make_response(jsonify({"message": "User already exists"}), 409)


class UserResource(Resource):
    """Operate on a single User, to view, update and delete it"""

    @swag_from('../docs/user/get.yml')
    def get(self, user_id):
        """Get a user"""

        sql = text("SELECT * FROM users WHERE id='{}'".format(user_id))
        user = db.engine.execute(sql)
        user_result = {'user': [dict(it) for it in user]}
        if user_result['user']:
            return make_response(jsonify(dict(user_result)), 200)

        return make_response(jsonify({"message": "User not found"}), 404)

    @swag_from('../docs/user/put.yml')
    def put(self, user_id):
        """Updates a user"""

        sql = text("SELECT * FROM users WHERE id='{}'".format(user_id))
        user = db.engine.execute(sql)
        user_result = {'user': [dict(it) for it in user]}
        if user_result['user']:
            args = user_request_parser.parse_args()

            invalid_input = validate_inputs(args)
            if invalid_input:
                return make_response(jsonify({"message": "{} must be a string of maximum {} characters".format(invalid_input[2], invalid_input[1])}), 400)

            first_name = args.get("first_name", None)
            last_name = args.get("last_name", None)
            username = args.get("username", None)

            # to avoid duplicating a user name
            sql = text(
                "SELECT * FROM users WHERE username='{}' LIMIT 1".format(username))
            user = db.engine.execute(sql)
            user_result = {'user': [dict(it) for it in user]}
            if not user_result['user'] or (user_result['user'] and (user_result['user']['id']== user_id)):
                sql = text("UPDATE users SET first_name='{}', last_name='{}', username='{}', updated_at=CURRENT_TIMESTAMP WHERE id='{}'".format(
                    first_name, last_name, username, user_id))
                db.engine.execute(sql)

                return make_response(jsonify({"message": "User updated"}), 200)

            return make_response(jsonify({"message": "User by that name already exists"}), 409)

        return make_response(jsonify({"message": "User not found"}), 404)

    @swag_from('../docs/user/delete.yml')
    def delete(self, user_id):
        """Delete a user"""

        sql = text("SELECT * FROM users WHERE id='{}'".format(user_id))
        user = db.engine.execute(sql)
        user_result = {'user': [dict(it) for it in user]}
        if user_result['user']:
            sql = text("DELETE FROM users WHERE id='{}'".format(user_id))
            db.engine.execute(sql)

            return make_response(jsonify({"message": "User deleted"}), 200)

        return make_response(jsonify({"message": "User not found"}), 404)
