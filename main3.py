from flask_restful import Api
from flask import Flask
from data import db_session, users_resource, rooms_resource, jobs_resource

app = Flask(__name__)
api = Api(app)


def main():
    db_session.global_init("db/blogs.db")
    # для списка объектов
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')

    # для одного объекта
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<users_id>')

    # для списка объектов
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')

    # для одного объекта
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<jobs_id>')

    # для списка объектов
    api.add_resource(rooms_resource.RoomsListResource, '/api/v2/rooms')

    # для одного объекта
    api.add_resource(rooms_resource.RoomsResource, '/api/v2/rooms/<rooms_id>')
    app.run()


if __name__ == '__main__':
    main()