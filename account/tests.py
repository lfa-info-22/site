
from lfainfo22.tests import ClientTestCase
from account.views   import LoginView, LogoutView
from django.test     import TestCase
from django.urls     import reverse

class LoginTest(ClientTestCase):
    VIEW = LoginView()

    ROUTE = f"/api/v{VIEW.VERSION}/{VIEW.APPLICATION}/{VIEW.ROUTE}"

    def test_can_login_username(self):
        username, email, password = ('user', 'user@test.com', 'password')
        response = self.anonymous_client.post(self.ROUTE, { 'user': username, 'password': password })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user.username, username)
        self.assertEqual(response.url, '/')

        self.anonymous_client.logout()

        response = self.anonymous_client.post(self.ROUTE, { 'user': email, 'password': password })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user.username, username)
        self.assertEqual(response.url, '/')

        self.anonymous_client.logout()

        response = self.anonymous_client.post(self.ROUTE, { 'user': username, 'password': 'A' })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user.username, '')
        self.assertEqual(response.url, reverse(self.VIEW.LOGIN_REDIRECTOR) + '?next=/')
    def test_redirect_keyword(self):
        username, email, password = ('user', 'user@test.com', 'password')
        NROUTE = self.ROUTE + '?' + self.VIEW.LOGIN_REDIRECTOR__NEXT_GET_ARG + '=' + '/url'

        response = self.anonymous_client.post(NROUTE, { 'user': username, 'password': 'A' })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user.username, '')
        self.assertEqual(response.url, reverse(self.VIEW.LOGIN_REDIRECTOR) + '?next=/url')

        response = self.anonymous_client.post(NROUTE, { 'user': username, 'password': password })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user.username, username)
        self.assertEqual(response.url, '/url')
    def test_json_resp_keyword(self):
        username, email, password = ('user', 'user@test.com', 'password')
        NROUTE = self.ROUTE + '?json_resp=true'

        response = self.anonymous_client.post(NROUTE, { 'user': username, 'password': 'A' })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user.username, '')
        self.assertEqual(response.json(), { 'status': False })

        response = self.anonymous_client.post(NROUTE, { 'user': username, 'password': password })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user.username, username)
        self.assertEqual(response.json(), { 'status': True })

class LogoutTest(ClientTestCase):
    VIEW = LogoutView()

    ROUTE = f"/api/v{VIEW.VERSION}/{VIEW.APPLICATION}/{VIEW.ROUTE}"

    def test_get_logout(self):
        response = self.client.get(self.ROUTE)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_anonymous)
        self.assertEqual(response.url, '/')

    def test_post_logout(self):
        response = self.client.post(self.ROUTE)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_anonymous)
        self.assertEqual(response.url, '/')

    def test_redirector(self):
        NROUTE = self.ROUTE + '?next=/url'

        response = self.client.post(NROUTE)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_anonymous)
        self.assertEqual(response.url, '/url')

        response = self.staff_client.get(NROUTE)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_anonymous)
        self.assertEqual(response.url, '/url')
    
    def test_json_resp(self):
        NROUTE = self.ROUTE + '?json_resp=true'

        response = self.client.post(NROUTE)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_anonymous)
        self.assertEqual(response.json(), { 'status': True })

        response = self.staff_client.get(NROUTE)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_anonymous)
        self.assertEqual(response.json(), { 'status': True })
