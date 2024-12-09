# Auth Middleware

## Overview

The Auth Middleware is a Flask-based application that provides an authentication service. It allows users to authenticate using their credentials (username and password) or a refresh token from any source. This project has been designed to be scalable and to run atomically as a microservice. The API utilizes the `/authenticate` route to handle the authentication logic and returns appropriate responses based on the authentication outcome.

## Features

*   User authentication using username and password.
*   Support for refresh tokens.

## Installation

To set up the application, follow these steps:

1.  **Clone the repository**:
    
    ```
    git clone https://github.com/grimimirg/auth-middleware.git
    cd auth-middleware
    ```
    
2.  **Create a virtual environment** (optional but recommended):
    
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    
3.  **Install the required packages**:
    
    ```
    pip install -r requirements.txt
    ```
    

## Usage

To run the application, execute the following command:

```
python app.py
```

The application will start on `http://127.0.0.1:5000/` by default.

## API Endpoints

### Authenticate User

*   **Endpoint**: `/authenticate`
*   **Method**: `POST`
*   **Request Body**: JSON object with the following fields:
    *   `username` (string, required): The username or email of the user.
    *   `password` (string, required): The password of the user.
    *   `refresh_token` (string, optional): A refresh token for re-authentication.

#### Example Request

1.  **Username and Password**:

   ```
   {
     "username": "user@example.com",
     "password": "securepassword"
   }
   ```

2.  **Refresh Token**:

   ```
   {
     "refresh_token": "<jwt_token>"
   }
   ```

#### Responses

*   **200 OK**: Successful authentication with user details.
    *   **Response Example**:
        
        ```
        {
          "accessToken": "<Generated JWT Token>",
          "expiresOn": ""
          "userId": "123456789",
          "refreshToken": "<Generated refresh JWT Token>"
        }
        ```
        
*   **400 Bad Request**: Missing required parameters if neither username/password nor refresh\_token is provided.
    *   **Response Example**:
        
        ```
        {
          "success": false,
          "message": "Missing required parameters."
        }
        ```
        

## Tests

To run tests, execute the following command in the application root folder:

   ```
   python -m unittest discover -s tests
   ```