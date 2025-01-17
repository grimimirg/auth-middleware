from flask import Flask
from flask_restful import Api

from controller.authentication_controller import AuthenticationController

app = Flask(__name__)
api = Api(app)

api.add_resource(AuthenticationController, '/authenticate')

if __name__ == '__main__':
    app.run()
