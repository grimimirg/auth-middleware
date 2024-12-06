# Authentication Middleware Controller

This project provides an authentication middleware controller built with Flask and Flask-RESTful. It handles user authentication requests, allowing users to authenticate using their credentials or a refresh token.

## Table of Contents

- Installation
- Usage
- API Endpoint
- Request Payload
- Responses
- Dependencies
- License

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   git clone <repository-url>
   cd <repository-directory>

2. Install the required packages:
   pip install -r requirements.txt

3. Ensure you have Python 3.x installed.

## Usage

To run the application, execute the following command:

python app.py

The application will start on http://127.0.0.1:5000/ by default.

## API Endpoint

The authentication controller exposes the following endpoint:

- POST /authenticate: Authenticates a user based on provided credentials.

## Request Payload

The request must include a JSON payload with the following fields:

- username (string): The username or email of the user.
- password (string): The password of the user.
- refresh_token (string, optional): A refresh token for re-authentication.

### Example Request

{
    "username": "user@example.com",
    "password": "yourpassword"
}

## Responses

The API will return a JSON response with an appropriate HTTP status code:

- 200 OK: Successful authentication with user details.
- 400 Bad Request: Missing required parameters if neither username/password nor refresh_token is provided.

### Example Response

TODO

## Dependencies

This project requires the following Python packages:

- Flask
- Flask-RESTful

You can install these dependencies using pip:

pip install Flask Flask-RESTful

## License

This project is licensed under the MIT License. See the LICENSE file for details.