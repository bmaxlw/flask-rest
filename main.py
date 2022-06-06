from http import client
from importlib.metadata import requires
from pydoc import cli
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:569782143@localhost:5432/cms_rest'

api = Api(app)
db = SQLAlchemy(app)

class ClientModel(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20))
    email_address = db.Column(db.String(50))

    def __repr__(self) -> str:
        return f"{self.client_id} {self.full_name} {self.phone_number} {self.email_address}"

# db.create_all()

clients = {}
client_args = reqparse.RequestParser()
client_args.add_argument("full_name", type=str, help='Full name undefined') # required=True
client_args.add_argument("phone_number", type=str, help='Phone number undefined') # required=True
client_args.add_argument("email_address", type=str, help='Email address undefined') # required=True

# serialize
resource_fields = {
    'client_id': fields.Integer,
    'full_name': fields.String,
    'phone_number': fields.String,
    'email_address': fields.String
}

def abort_if_id_not_exists(client_id):
    if not ClientModel.query.get(client_id):
        abort(404, message='Client does not exist...')

def abort_if_id_exists(client_id):
    if ClientModel.query.get(client_id):
        abort(409, message='Client already exists...')

class Client(Resource):
    @marshal_with(resource_fields)
    def get(self, client_id):
        abort_if_id_not_exists(client_id)
        result = ClientModel.query.filter_by(client_id=client_id).first()
        return result

    def post(self, client_id):
        abort_if_id_exists(client_id)
        args = client_args.parse_args()
        client = ClientModel(client_id=client_id, full_name=args['full_name'], phone_number=args['phone_number'], email_address=args['email_address'])
        db.session.add(client)
        db.session.commit()
        return {'message': 'Client added...'}

    def put(self, client_id):
        args = client_args.parse_args()
        client = ClientModel.query.filter_by(client_id=client_id).first()
        if args['full_name']:
            client.full_name = args['full_name']
        if args['phone_number']:
            client.phone_number = args['phone_number']
        if args['email_address']:
            client.email_address = args['email_address']
        db.session.merge(client)
        db.session.commit()
        return {'message': 'Client updated...'}

    def delete(self, client_id):
        abort_if_id_not_exists(client_id)
        client = ClientModel.query.filter_by(client_id=client_id).first()
        db.session.delete(client)
        db.session.commit()
        return {'message': 'Client was deleted...'}

api.add_resource(Client, '/clients/<int:client_id>')

if __name__ == '__main__':
    app.run(debug=True)
