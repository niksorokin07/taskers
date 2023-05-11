from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, request, jsonify
from .users import User
from data import db_session
from werkzeug.security import generate_password_hash


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


def abort_if_users_not_int(user_id):
    if not user_id.isdigit():
        abort(400, message=f"Bad request")


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_users_not_int(users_id)
        users_id = int(users_id)
        print('qwert')
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        news = session.query(User).get(users_id)
        return jsonify({'users': news.to_dict(
            only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password_hash'))})

    def delete(self, users_id):
        abort_if_users_not_int(users_id)
        users_id = int(users_id)
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        news = session.query(User).get(users_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password_hash')) for
            item in news]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("surname", type=str)
        parser.add_argument("name", type=str)
        parser.add_argument("age", type=int)
        parser.add_argument("position", type=str)
        parser.add_argument("speciality", type=str)
        parser.add_argument("address", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str)
        args = parser.parse_args()
        session = db_session.create_session()
        if args["surname"] and args["name"] and args["age"] and args["position"] and args[
            "speciality"] and args["address"] and args["email"] and args["password"]:
            users = User()
            users.surname = args["surname"]
            users.name = args["name"]
            users.age = args["age"]
            users.position = args["position"]
            users.speciality = args["speciality"]
            users.address = args["address"]
            users.email = args["email"]
            users.password_hash = generate_password_hash(args["password"])
            session.add(users)
            session.commit()
            return jsonify({'success': 'OK'})
        else:
            return jsonify({'error': 'Not all arguments'})