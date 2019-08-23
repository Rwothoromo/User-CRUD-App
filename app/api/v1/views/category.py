from flask import jsonify, make_response, request, session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flasgger import swag_from
from sqlalchemy.sql import text

from app.db import db
from app.models.category import Category
from app.api.v1.helpers import validate_inputs


# RequestParser and added arguments will know which fields to accept and how to validate those
category_request_parser = RequestParser(bundle_errors=True)
category_request_parser.add_argument(
    "name", type=str, required=True, help="Name must be a valid string")


class CategoryCollection(Resource):
    """Operate on a list of categories, to view and add them"""

    @swag_from('../docs/category/post.yml')
    def post(self):
        """Register a category"""

        args = category_request_parser.parse_args()

        invalid_input = validate_inputs(args)
        if invalid_input:
            return make_response(jsonify({"message": "{} must be a string of maximum {} characters".format(invalid_input[2], invalid_input[1])}), 400)

        name = args.get("name", None)

        sql = text(
            "SELECT * FROM categories WHERE name='{}' LIMIT 1".format(name))
        category = db.engine.execute(sql)
        category_result = {'category': [dict(it) for it in category]}
        if not category_result['category']:
            sql = text(
                "INSERT into categories (name) VALUES ('{}')".format(name))
            db.engine.execute(sql)

            return make_response(
                jsonify({"message": "Category added"}), 201)

        return make_response(jsonify({"message": "Category already exists"}), 409)


class CategoryResource(Resource):
    """Operate on a single Category, to view, update and delete it"""

    @swag_from('../docs/category/delete.yml')
    def delete(self, category_id):
        """Delete a category"""

        sql = text("SELECT * FROM categories WHERE id='{}'".format(category_id))
        category = db.engine.execute(sql)
        category_result = {'category': [dict(it) for it in category]}
        if category_result['category']:
            sql = text(
                "DELETE FROM categories WHERE id='{}'".format(category_id))
            db.engine.execute(sql)

            return make_response(jsonify({"message": "Category deleted"}), 200)

        return make_response(jsonify({"message": "Category not found"}), 404)
