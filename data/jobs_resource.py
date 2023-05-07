from flask_restful import reqparse , abort , Api , Resource
from flask import Flask , request , jsonify
from .jobs import Jobs
from data import db_session


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    news = session.query(Jobs).get(jobs_id)
    if not news:
        abort(404 , message=f"Job {jobs_id} not found")


def abort_if_jobs_not_int(jobs_id):
    if not jobs_id.isdigit():
        abort(400 , message=f"Bad request")


class JobsResource(Resource):
    def get(self , jobs_id):
        abort_if_jobs_not_int(jobs_id)
        jobs_id = int(jobs_id)
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        news = session.query(Jobs).get(jobs_id)
        return jsonify({'Jobs': news.to_dict(
            only=(
            'id' , 'team_leader' , 'job' , 'work_size' , 'collaborators' , 'start_date' , 'end_date' , 'is_finished'))})

    def delete(self , jobs_id):
        abort_if_jobs_not_int(jobs_id)
        jobs_id = int(jobs_id)
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        news = session.query(Jobs).get(jobs_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Jobs).all()
        return jsonify({'Jobs': [item.to_dict(
            only=(
            'id' , 'team_leader' , 'job' , 'work_size' , 'collaborators' , 'start_date' , 'end_date' , 'is_finished'))
            for item in news]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("team_leader" , type=int)
        parser.add_argument("job" , type=str)
        parser.add_argument("work_size" , type=int)
        parser.add_argument("collaborators" , type=str)
        parser.add_argument("is_finished" , type=bool)
        args = parser.parse_args()
        session = db_session.create_session()
        if args["team_leader"] and args["job"] and args["work_size"] and args["collaborators"]:
            jobs = Jobs()
            jobs.team_leader = args["team_leader"]
            jobs.job = args["job"]
            jobs.work_size = args["work_size"]
            jobs.collaborators = args["collaborators"]
            jobs.is_finished = args["is_finished"]
            session.add(jobs)
            session.commit()
            return jsonify({'success': 'OK'})
        else:
            return jsonify({'error': 'Not all arguments'})
