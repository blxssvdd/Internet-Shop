import os
import binascii
from datetime import timedelta

from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from flask_migrate import Migrate

from src.database.base import db
from src.database import db_actions


load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_URI")
app.config["JWT_SECRET_KEY"] = binascii.hexlify(os.urandom(24))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
db.init_app(app)
api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


# with app.app_context():
#     db.create_all()



class ProductAPI(Resource):
    def get(self, product_id: str|None = None):
        if product_id:
            product = db_actions.get_product(product_id)
            response = jsonify(product)
        else:
            products = db_actions.get_products()
            response = jsonify(products)

        response.status_code = 201
        return response

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument("name")
        parse.add_argument("description")
        parse.add_argument("img_url")
        parse.add_argument("price")
        kwargs = parse.parse_args()
        prod_id = db_actions.add_product(**kwargs)
        response = jsonify(dict(product_id=prod_id))
        response.status_code = 201
        return response

    def put(self, product_id: str):
        parse = reqparse.RequestParser()
        parse.add_argument("name")
        parse.add_argument("description")
        parse.add_argument("price")
        parse.add_argument("img_url")
        kwargs = parse.parse_args()
        msg = db_actions.edit_product(**kwargs)
        response = jsonify(msg)
        response.status_code = 201
        return response

    def delete(self, product_id: str):
        msg = db_actions.del_product(product_id)
        response = jsonify(msg)
        response.status_code - 201
        return response




class ReviewAPI(Resource):
    def row_db_to_json(self, reviews: list):
        data = []
        for review in reviews:
            data.append({
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "author": review.author
            })

        data_json = jsonify(data)
        data_json.status_code = 201
        return data_json

    def get(self, review_id: str|None = None):
        if review_id:
            review = db_actions.get_review(review_id)
            return self.row_db_to_json([review])
        else:
            reviews = db_actions.get_reviews()
            return self.row_db_to_json(reviews)

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument("text")
        parse.add_argument("rating")
        parse.add_argument("author")
        args = parse.parse_args()
        rev_id = db_actions.add_review(
            text=args.get("text"),
            rating=args.get("rating"),
            author=args.get("author")
        )
        response = jsonify(dict(review_id=rev_id))
        response.status_code - 201
        return response

    def put(self, review_id: str):
        parse = reqparse.RequestParser()
        parse.add_argument("text")
        parse.add_argument("rating")
        parse.add_argument("author")
        args = parse.parse_args()
        msg = db_actions.edit_review(
            rev_id=review_id,
            text=args.get("text"),
            rating=args.get("rating"),
            author=args.get("author")
        )
        response = jsonify(msg)
        response.status_code = 201
        return response

    def delete(self, review_id: str):
        msg = db_actions.del_review(review_id)
        response = jsonify(msg)
        response.status_code - 201
        return response


class UserAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = db_actions.get_user(user_id)
        # user ._password = ""


        response = jsonify(user)
        user = response.json
        del user["_password"]
        response.status_code = 200
        return response

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("first_name")
        parser.add_argument("last_name")
        parser.add_argument("email")
        parser.add_argument("password")
        kwargs = parser.parse_args()
        msg = db_actions.add_user(**kwargs)
        response = jsonify(msg)
        response.status_code = 201
        return response


class TokenAPI(Resource):
    @jwt_required(refresh=True)
    def get(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        response = jsonify(dict(access_token=access_token))
        response.status_code = 200
        return response


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        parser.add_argument("password")
        kwargs = parser.parse_args()
        tokens = db_actions.get_tokens(**kwargs)
        response = jsonify(tokens)
        response.status_code = 200
        return response


api.add_resource(ProductAPI, "/api/products/", "/api/products/<product_id>")
api.add_resource(ReviewAPI, "/api/reviews/", "/api/reviews/<review_id>")
api.add_resource(UserAPI, "/api/user/")
api.add_resource(TokenAPI, "/api/token/")

if __name__ == "__main__":
    app.run(debug=True, port=3001)
    