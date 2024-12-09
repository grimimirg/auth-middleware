import unittest
from unittest.mock import patch, MagicMock
from src.services.jwt_service import JwtService
from src.model.authenticated_response import AuthenticateResponse
from src.model.authenticated_user import AuthenticatedUser
from src.services.constants_service import ConstantsService

class JwtServiceTest(unittest.TestCase):

    def setUp(self):
        self.secret = "test_secret"
        self.jwt_util = JwtService(self.secret)

    @patch('src.services.user_service.UserService')
    @patch('src.util.secure_util.SecureUtil')
    @patch('jwt.decode')
    def test_parse_token_success(self, mock_jwt_decode, mock_secure_util, mock_user_service):
        # GIVEN
        token = "valid_token"
        user_id = 1
        mock_jwt_decode.return_value = {'sub': str(user_id)}
        mock_secure_util.decode.return_value = str(user_id)
        user = MagicMock(id=user_id)
        mock_user_service.getUserByCode.return_value = user

        # WHEN
        result = self.jwt_util.parseToken(token)

        # THEN
        self.assertIsInstance(result, AuthenticatedUser)
        self.assertEqual(result.subject, str(user_id))
        self.assertEqual(result.user, user)

    @patch('jwt.decode')
    def test_parse_token_invalid(self, mock_jwt_decode):
        # GIVEN
        token = "invalid_token"
        mock_jwt_decode.side_effect = Exception("Invalid token")

        # WHEN
        result = self.jwt_util.parseToken(token)

        # THEN
        self.assertIsNone(result)

    def test_generate_token(self):
        # GIVEN
        user_id = "1"
        expiration = datetime.now() + timedelta(days=1)
        is_refresh_token = False
        password = "password"

        # WHEN
        token = self.jwt_util.generateToken(user_id, expiration, is_refresh_token, password)

        # THEN
        self.assertIsInstance(token, str)

    @patch('src.util.secure_util.SecureUtil')
    @patch('jwt.encode')
    def test_generate_authenticate_response(self, mock_jwt_encode, mock_secure_util):
        # GIVEN
        user_id = "1"
        mock_secure_util.encode.return_value = user_id
        mock_jwt_encode.side_effect = ["access_token", "refresh_token"]
        ConstantsService.TOKEN_EXPIRATION_DAYS = 1
        ConstantsService.REFRESH_TOKEN_EXPIRATION_DAYS = 1

        # WHEN
        response = self.jwt_util.generateAuthenticateResponse(user_id)

        # THEN
        self.assertIsInstance(response, AuthenticateResponse)
        self.assertEqual(response.accessToken, "access_token")
        self.assertEqual(response.refreshToken, "refresh_token")
        self.assertEqual(response.userId, int(user_id))

    @patch('flask.request')
    def test_get_request_jwt(self, mock_request):
        # GIVEN
        mock_request.headers = {'Authorization': 'Bearer token'}

        # WHEN
        result = self.jwt_util.getRequestJwt()

        # THEN
        self.assertEqual(result, 'Bearer token')

    @patch('flask.request')
    @patch('jwt.decode')
    def test_get_jwt_attribute(self, mock_jwt_decode, mock_request):
        # GIVEN
        mock_request.headers = {'Authorization': 'Bearer token'}
        mock_jwt_decode.return_value = {'attribute': 'value'}

        # WHEN
        result = self.jwt_util.getJwtAttribute('attribute')

        # THEN
        self.assertEqual(result, 'value')

if __name__ == '__main__':
    unittest.main()
