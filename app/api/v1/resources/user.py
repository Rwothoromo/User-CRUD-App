# app/api/resources/user.py

from flask import jsonify, make_response, request, session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flasgger import swag_from
from sqlalchemy.sql import text

from app.db import db
from app.models.user import User


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


def validate_inputs(args):
    """Return error message if input is invalid"""

    fifty_character_limit = ['first_name', 'last_name', 'username']
    for key, value in args.items():
        valid_length = 50 if key in fifty_character_limit else 256
        arg_is_invalid = (len(value) > valid_length or not isinstance(value, str) or not value.strip(),
                          valid_length, key)
        if arg_is_invalid[0]:
            return arg_is_invalid

# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class UserCollection(Resource):
    """Operate on a list of users, to view and add them"""

    @swag_from('docs/get_users.yml')
    def get(self):
        """Retrieves all users"""

        args = q_request_parser.parse_args()
        q = args.get('q', None)

        if q:
            q = q.lower()
            sql = text("SELECT * FROM users WHERE username like '%{}%'".format(q))
        else:
            sql = text("SELECT * FROM users ORDER BY username ASC")

        users = db.engine.execute(sql)
        if not users:
            return make_response(jsonify({"message": "No user found"}), 404)

        users_result = {'users': [dict(user) for user in users]}

        return make_response(jsonify(users_result), 200)

    @swag_from('docs/post_user.yml')
    def post(self):
        """Register a user"""

        args = user_request_parser.parse_args()

        invalid_input = validate_inputs(args)
        if invalid_input:
            return make_response(jsonify({"message": "{} must be a string of maximum {} characters".format(invalid_input[2], invalid_input[1])}), 400)

        first_name = args.get("first_name", None)
        last_name = args.get("last_name", None)
        username = args.get("username", None)

        user = User.query.filter_by(username=username).first()
        if not user:
            sql = text("INSERT into users (first_name, last_name, username) VALUES ('{}', '{}', '{}')".format(
                first_name, last_name, username))
            db.engine.execute(sql)

            return make_response(
                jsonify({"message": "User added"}), 201)

        return make_response(jsonify({"message": "User already exists"}), 409)


class UserResource(Resource):
    """Operate on a single User, to view, update and delete it"""

    @swag_from('docs/get_user.yml')
    def get(self, user_id):
        """Get a user"""

        user = User.query.get(user_id)
        if user:
            return make_response(jsonify(user.user_as_dict()), 200)

        return make_response(jsonify({"message": "User not found"}), 404)

    @swag_from('docs/put_user.yml')
    def put(self, user_id):
        """Updates a user"""

        user = User.query.get(user_id)
        if user:
            args = user_request_parser.parse_args()

            invalid_input = validate_inputs(args)
            if invalid_input:
                return make_response(jsonify({"message": "{} must be a string of maximum {} characters".format(invalid_input[2], invalid_input[1])}), 400)

            first_name = args.get("first_name", None)
            last_name = args.get("last_name", None)
            username = args.get("username", None)

            # to avoid duplicating a user name
            user_by_name = User.query.filter_by(username=username).first()
            if not user_by_name or (user_by_name and (user_by_name.id == user_id)):
                user.first_name = first_name
                user.last_name = last_name
                user.username = username

                db.session.commit()

                return make_response(jsonify({"message": "User updated"}), 200)

            return make_response(jsonify({"message": "User by that name already exists"}), 409)

        return make_response(jsonify({"message": "User not found"}), 404)

    @swag_from('docs/delete_user.yml')
    def delete(self, user_id):
        """Delete a user"""

        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

            return make_response(jsonify({"message": "User deleted"}), 200)

        return make_response(jsonify({"message": "User not found"}), 404)
