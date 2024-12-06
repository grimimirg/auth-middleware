import jwt
import base64

from user_service import UserService
from constants_service import ConstantsService

from model.authenticated_response import AuthenticateResponse
from model.authenticated_user import AuthenticatedUser

from datetime import datetime, timedelta
from flask import request
from util.secure_util import SecureUtil

class JwtUtil:
    """
    JwtUtil provides utility functions for handling JSON Web Tokens (JWT).
    
    This class includes methods for generating, parsing, and managing JWTs for user authentication.
    """

    def __init__(self, secret):
        """
        Initializes the JwtUtil with a secret key for signing tokens.

        Args:
            secret (str): The secret key used for signing JWTs.
        """
        self.secret = secret

    def parseToken(self, token):
        """
        Parses a JWT and returns an AuthenticatedUser object if the token is valid.

        Args:
            token (str): The JWT to be parsed.

        Returns:
            AuthenticatedUser: An object representing the authenticated user if the token is valid,
                               None if the token is invalid or an error occurs.
        """
        try:
            body = jwt.decode(token, ConstantsService.SECRET, algorithms=["HS512"])
            authenticatedUser = AuthenticatedUser(
                subject=body['sub'],
                token=token,
                user=UserService.getUserByCode(int(SecureUtil.decode(body['sub']))),
                additionalInfo=None
            )
            return authenticatedUser
        except Exception as ex:
            return None

    def generateToken(self, userId, expiration, isRefreshToken, password=None):
        """
        Generates a JWT for a user with specified claims.

        Args:
            userId (str): The ID of the user for whom the token is generated.
            expiration (datetime): The expiration date and time of the token.
            isRefreshToken (bool): Indicates if the token is a refresh token.
            password (str, optional): The user's password, included in the token if provided.

        Returns:
            str: The generated JWT as a string.
        """
        claims = {
            'sub': userId,
            'expiration': expiration,
            'refresh': isRefreshToken
        }
        if password:
            claims['password'] = password

        return jwt.encode(claims, self.secret, algorithm="HS512")

    def generateAuthenticateResponse(self, userId, password=None):
        """
        Generates an authentication response containing access and refresh tokens.

        Args:
            userId (str): The ID of the user for whom the tokens are generated.
            password (str, optional): The user's password, included in the tokens if provided.

        Returns:
            AuthenticateResponse: An object containing the access token, refresh token, 
                                  expiration date, and user ID.
        """
        userId = SecureUtil.encode(userId)

        response = AuthenticateResponse()

        authTokenExpirationDate = datetime.now() + timedelta(days=int(ConstantsService.TOKEN_EXPIRATION_DAYS))
        refreshTokenExpirationDate = datetime.now() + timedelta(days=int(ConstantsService.REFRESH_TOKEN_EXPIRATION_DAYS))

        response.accessToken = self.generateToken(userId, authTokenExpirationDate, False, password)
        response.expiresOn = authTokenExpirationDate
        response.userId = int(SecureUtil.decode(userId))
        response.refreshToken = self.generateToken(userId, refreshTokenExpirationDate, True, password)

        return response

    @staticmethod
    def getRequestJwt():
        """
        Retrieves the JWT from the Authorization header of the current request.

        Returns:
            str: The JWT from the Authorization header, or None if not present.
        """
        return request.headers.get('Authorization')

    @staticmethod
    def getJwtAttribute(attribute):
        """
        Extracts a specific attribute from the JWT in the Authorization header.

        Args:
            attribute (str): The name of the attribute to extract from the JWT.

        Returns:
            Any: The value of the specified attribute from the JWT, or None if not found.
        """
        requestJwt = JwtUtil.getRequestJwt()
        decoded = base64.b64decode(requestJwt).decode('utf-8')
        jwtData = jwt.decode(decoded[15:], options={"verify_signature": False})  # Skip signature verification for attribute extraction
        return jwtData.get(attribute)
