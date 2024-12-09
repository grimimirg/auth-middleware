import unittest
from unittest.mock import patch, MagicMock
from src.services.authentication_service import AuthenticationService
from src.response.api_response import ApiResponse

class AuthenticationServiceTest(unittest.TestCase):

    def setUp(self):
        self.auth_service = AuthenticationService()

    @patch('src.services.user_service.UserService')
    def test_password_changed(self, mock_user_service):
        # GIVEN
        user_id = 1
        password = "new_password"
        mock_user_service.getUserById.return_value = MagicMock(password="old_password")

        # WHEN
        result = self.auth_service.passwordChanged(user_id, password)

        # THEN
        self.assertTrue(result)

    @patch('src.services.user_service.UserService')
    @patch('src.services.jwt_service.JwtService')
    @patch('src.util.secure_util.SecureUtil')
    def test_authenticate_success(self, mock_secure_util, mock_jwt_util, mock_user_service):
        # GIVEN
        user_credentials = MagicMock(username="test@example.com", password="password", refreshToken=None)
        user = MagicMock(id=1, email="test@example.com", password="encoded_password", active=True, email_verified=True)
        mock_user_service.getUserByEmail.return_value = user
        mock_secure_util.encode.return_value = "encoded_password"
        mock_jwt_util.generateAuthenticateResponse.return_value = "jwt_response"

        # WHEN
        result = self.auth_service.authenticate(user_credentials)

        # THEN
        self.assertEqual(result, "jwt_response")
        mock_user_service.getUserByEmail.assert_called_once_with("test@example.com")

    @patch('src.services.user_service.UserService')
    def test_authenticate_user_not_found(self, mock_user_service):
        # GIVEN
        user_credentials = MagicMock(username="notfound@example.com", password="password", refreshToken=None)
        mock_user_service.getUserByEmail.return_value = None

        # WHEN
        result = self.auth_service.authenticate(user_credentials)

        # THEN
        self.assertEqual(result, ApiResponse.getResponse(ApiResponse.NOT_FOUND))

    @patch('src.services.user_service.UserService')
    @patch('src.util.secure_util.SecureUtil')
    def test_authenticate_user_not_active(self, mock_secure_util, mock_user_service):
        # GIVEN
        user_credentials = MagicMock(username="test@example.com", password="password", refreshToken=None)
        user = MagicMock(id=1, email="test@example.com", password="encoded_password", active=False, email_verified=True)
        mock_user_service.getUserByEmail.return_value = user

        # WHEN
        result = self.auth_service.authenticate(user_credentials)

        # THEN
        self.assertEqual(result, ApiResponse.getResponse(ApiResponse.USER_NOT_ACTIVE))

    @patch('src.services.user_service.UserService')
    @patch('src.util.secure_util.SecureUtil')
    def test_authenticate_user_not_verified(self, mock_secure_util, mock_user_service):
        # GIVEN
        user_credentials = MagicMock(username="test@example.com", password="password", refreshToken=None)
        user = MagicMock(id=1, email="test@example.com", password="encoded_password", active=True, email_verified=False)
        mock_user_service.getUserByEmail.return_value = user

        # WHEN
        result = self.auth_service.authenticate(user_credentials)

        # THEN
        self.assertEqual(result, ApiResponse.getResponse(ApiResponse.USER_NOT_VERIFIED))

    @patch('src.services.user_service.UserService')
    @patch('src.util.secure_util.SecureUtil')
    def test_authenticate_wrong_password(self, mock_secure_util, mock_user_service):
        # GIVEN
        user_credentials = MagicMock(username="test@example.com", password="wrong_password", refreshToken=None)
        user = MagicMock(id=1, email="test@example.com", password="encoded_password", active=True, email_verified=True)
        mock_user_service.getUserByEmail.return_value = user
        mock_secure_util.encode.return_value = "different_encoded_password"

        # WHEN
        result = self.auth_service.authenticate(user_credentials)

        # THEN
        self.assertEqual(result, ApiResponse.getResponse(ApiResponse.WRONG_PASSWORD))

if __name__ == '__main__':
    unittest.main()
