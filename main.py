from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

clients = {
    10000: {'full_name': 'James Robertson', 'phone_number': '+420-555-88-99', 'email_address': 'jrobertson@ico.cz'} 
}

class Client(Resource):
    def get(self, client_id):
        return clients[client_id]

api.add_resource(Client, 'clients/<int:client_id>')

if __name__ == '__main__':
    app.run(debug=True)

