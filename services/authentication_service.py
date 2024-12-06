from services.jwt_service import JwtUtil
from services.user_service import UserService

from response.api_response import ApiResponse

from util.secure_util import SecureUtil

import base64
import json

class AuthenticationService:
    """
    AuthenticationService handles user authentication and password management.
    
    This service provides methods to authenticate users based on their credentials,
    check if a password has changed, and manage JWT tokens for secure communication.
    """

    def passwordChanged(self, userId, password):
        """
        Checks if the password for a given user has changed.

        Args:
            userId (int): The ID of the user whose password is being checked.
            password (str): The password to compare against the stored password.

        Returns:
            bool: True if the provided password is different from the stored password, 
                  False otherwise.
        """
        user = UserService.getUserById(userId)
        return password != user.password

    def authenticate(self, userCredentials):
        """
        Authenticates a user based on provided credentials, which may include a refresh token.

        Args:
            userCredentials (object): An object containing user credentials, which may include:
                - username (str): The email or username of the user.
                - password (str): The password of the user.
                - refreshToken (str): An optional JWT refresh token.

        Returns:
            ApiResponse: An API response object indicating the result of the authentication process.
                Possible responses include:
                - INVALID_JWT_TOKEN: If the refresh token is invalid or cannot be decoded.
                - NOT_FOUND: If the user is not found.
                - USER_NOT_ACTIVE: If the user account is not active.
                - USER_NOT_VERIFIED: If the user's email is not verified.
                - WRONG_PASSWORD: If the password is incorrect or has changed.
                - An authenticated JWT response if authentication is successful.
        """
        decodedToken = None
        tokenData = None

        try:
            if userCredentials.refreshToken:
                decodedToken = base64.b64decode(userCredentials.refreshToken).decode('utf-8')
                tokenData = json.loads(decodedToken[15:])
            else:
                tokenData = None
        except Exception as e:
            return ApiResponse.getResponse(ApiResponse.INVALID_JWT_TOKEN)

        decode = userCredentials.refreshToken and self.decodeToken(tokenData.get("sub"))
        
        user = (
                UserService.getUserById(int(decode)) 
                if userCredentials.refreshToken 
                else UserService.getUserByEmail(userCredentials.username)
            )

        if user is None:
            return ApiResponse.getResponse(ApiResponse.NOT_FOUND)

        userCredentials.username = user.email

        if user.active is None or not user.active:
            return ApiResponse.getResponse(ApiResponse.USER_NOT_ACTIVE)

        if user.email_verified is None or not user.email_verified:
            return ApiResponse.getResponse(ApiResponse.USER_NOT_VERIFIED)

        if userCredentials.refreshToken:
            decode = SecureUtil.decode(tokenData.get("sub"))
            passwordChanged = self.passwordChanged(int(decode), tokenData.get("password"))

            if passwordChanged:
                return ApiResponse.getResponse(ApiResponse.WRONG_PASSWORD)
        else:
            try:
                pwd = SecureUtil.encode(userCredentials.password)
            except Exception as e:
                return ApiResponse.getResponse(ApiResponse.INTERNAL_SERVER_ERROR)

            if user.password != pwd:
                return ApiResponse.getResponse(ApiResponse.WRONG_PASSWORD)

        return JwtUtil.generateAuthenticateResponse(str(user.id), user.password)
