from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, request, jsonify
from .rooms import Room
from data import db_session


def abort_if_rooms_not_found(rooms_id):
    session = db_session.create_session()
    news = session.query(Room).get(rooms_id)
    if not news:
        abort(404, message=f"Room {rooms_id} not found")


def abort_if_rooms_not_int(rooms_id):
    if not rooms_id.isdigit():
        abort(400, message=f"Bad request")


class RoomsResource(Resource):
    def get(self, rooms_id):
        abort_if_rooms_not_int(rooms_id)
        rooms_id = int(rooms_id)
        abort_if_rooms_not_found(rooms_id)
        session = db_session.create_session()
        news = session.query(Room).get(rooms_id)
        return jsonify({'Rooms': news.to_dict(
            only=('id', 'title', 'about', 'team_leader', 'tasks', 'collaborators'))})

    def delete(self, rooms_id):
        abort_if_rooms_not_int(rooms_id)
        rooms_id = int(rooms_id)
        abort_if_rooms_not_found(rooms_id)
        session = db_session.create_session()
        news = session.query(Room).get(rooms_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class RoomsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Room).all()
        return jsonify({'Rooms': [item.to_dict(
            only=('id', 'title', 'about', 'team_leader', 'tasks', 'collaborators'))
            for item in news]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str)
        parser.add_argument("about", type=str)
        parser.add_argument("team_leader", type=int)
        parser.add_argument("tasks", type=str)
        parser.add_argument("collaborators", type=str)
        args = parser.parse_args()
        session = db_session.create_session()
        if args["title"] and args["about"] and args["team_leader"] and args["tasks"] and args["collaborators"]:
            rooms = Room()
            rooms.team_leader = args["team_leader"]
            rooms.title = args["title"]
            rooms.about = args["about"]
            rooms.collaborators = args["collaborators"]
            rooms.tasks = args["tasks"]
            session.add(rooms)
            session.commit()
            return jsonify({'success': 'OK'})
        else:
            return jsonify({'error': 'Not all arguments'})
