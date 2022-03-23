
from lfainfo22.tests import ClientTestCase
from account.views   import LoginView
from django.test     import TestCase

class LoginTest(ClientTestCase):
    VIEW = LoginView()

    ROUTE = f"/api/v{VIEW.VERSION}/{VIEW.APPLICATION}/{VIEW.ROUTE}"

    def test_can_login_username(self):
        username, email, password = ('user', 'user@test.com', 'password')
        response = self.anonymous_client.post(self.ROUTE, { 'user': username, 'password': password })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.user.username, username)
