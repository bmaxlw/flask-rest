from http import client
from importlib.metadata import requires
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

clients = {}

client_args = reqparse.RequestParser()
client_args.add_argument("full_name", type=str, help='Full name undefined', required=True)
client_args.add_argument("phone_number", type=str, help='Phone number undefined', required=True)
client_args.add_argument("email_address", type=str, help='Email address undefined', required=True)

def abort_if_id_not_exists(client_id):
    if client_id not in clients:
        abort(404, message='Client does not exist...')

def abort_if_id_exists(client_id):
    if client_id in clients:
        abort(409, message='Client already exists...')

class Client(Resource):
    def get(self, client_id):
        abort_if_id_not_exists(client_id)
        return {client_id: clients[client_id]}

    def put(self, client_id):
        abort_if_id_exists(client_id)
        args = client_args.parse_args()
        clients[client_id] = args
        return {'message': 'Client was added...'}

    def delete(self, client_id):
        abort_if_id_not_exists(client_id)
        del clients[client_id]
        return {'message': 'Client was deleted...'}

api.add_resource(Client, '/clients/<int:client_id>')

if __name__ == '__main__':
    app.run(debug=True)

