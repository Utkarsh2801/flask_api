import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True,
                        type=str, help="username required")
    parser.add_argument("password", required=True,
                        type=str, help="password required")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "user already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User Created Successfully."}, 201
