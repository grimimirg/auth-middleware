from flask import jsonify

class ApiResponse:
    
    OK = {"code": 1, "http_code": "200", "message": "OK" }
    INTERNAL_SERVER_ERROR = {"code": 2, "http_code": "500", "message": "Internal server error" }
    MISSING_PARAMETER = {"code": 3, "http_code": "400", "message": "Required parameter missing" }
    MISSING_CLIENT_ID_HEADER = {"code": 4, "http_code": "403", "message": "The request doesn't contain a correct header with the client id" }
    MISSING_JWT_HEADER = {"code": 5, "http_code": "403", "message": "JWT token missing in the request" }
    INVALID_JWT_TOKEN = {"code": 6, "http_code": "403", "message": "The request contains an invalid JWT token" }
    EXPIRED_JWT_TOKEN = {"code": 7, "http_code": "403", "message": "The request contains an expired JWT token" }
    NOT_FOUND = {"code": 8, "http_code": "404", "message": "The content requested can't be found" }
    USER_ALREADY_EXISTS = {"code": 9, "http_code": "409", "message": "The user already exists" }
    WRONG_PASSWORD = {"code": 10, "http_code": "401", "message": "Wrong password" }
    UNAUTHORIZED = {"code": 11, "http_code": "401", "message": "User unauthorized" }
    CHANGE_PASSWORD_NOT_AVAILABLE = {"code": 12, "http_code": "401", "message": "Change password not available" }
    USER_NOT_VERIFIED = {"code": 13, "http_code": "401", "message": "Email exists but it hasn't yet been verified" }
    USER_NOT_ACTIVE = {"code": 14, "http_code": "401", "message": "User not active" }
    USER_CANNOT_BE_FOUND = {"code": 15, "http_code": "404", "message": "User cannot be found" }
    INVALID_INPUT_VALUE = {"code": 16, "http_code": "400 ", "message": "Invalid input value" }

    @staticmethod
    def getResponse(body):
          bodyJson = jsonify(body)
          return bodyJson, bodyJson.http_code