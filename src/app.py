from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from services.authentication_service import AuthenticationService
from response.api_response import ApiResponse

app = Flask(__name__)
api = Api(app)

class AuthenticationController(Resource):
    """
    AuthenticationController handles user authentication requests.

    This controller provides an endpoint for users to authenticate using their credentials
    or a refresh token. It utilizes the AuthenticationService to process authentication logic.
    """

    def __init__(self):
        """
        Initializes the AuthenticationController with an instance of AuthenticationService.
        """
        self.authentication_service = AuthenticationService()

    def post(self):
        """
        Authenticates a user based on provided credentials.

        Expects a JSON payload in the request body with the following fields:
        - username (str): The username or email of the user.
        - password (str): The password of the user.
        - refresh_token (str, optional): A refresh token for re-authentication.

        Returns:
            Response: A JSON response containing the authentication result, along with an HTTP status code.
                Possible responses include:
                - 200: Successful authentication with user details.
                - 400: Missing required parameters if neither username/password nor refresh_token is provided.
        """
        user_credentials = request.get_json()

        if (not user_credentials.get('username') or not user_credentials.get('password')) and not user_credentials.get('refresh_token'):
            return ApiResponse.getResponse(ApiResponse.MISSING_PARAMETER), 400

        response = self.authentication_service.authenticate(user_credentials)
        return jsonify(response), 200

api.add_resource(AuthenticationController, '/authenticate')

if __name__ == '__main__':
    app.run(debug=True)
