from django.test import TestCase, Client
from account.models import User

class ClientTestCase(TestCase):
    def setUp(self) -> None:
        self.staff_client = Client()
        self.staff_user = User.objects.create_user('staff', 'staff@test.com', 'password')
        self.staff_user.is_staff = True
        self.staff_user.save()

        self.client = Client()
        self.user = User.objects.create_user('user', 'user@test.com', 'password')

        self.staff_client.login(username='staff', password='password')
        self.client.login(username='user', password='password')

        self.anonymous_client = Client()

        return super().setUp()
        
    def send_staff_request(self, url, ctx):
        self.send_request(url, ctx, expected_staff=200, expected_lambda=404, expected_anonymous=404)
    def send_lambda_request(self, url, ctx):
        self.send_request(url, ctx, expected_staff=200, expected_lambda=200, expected_anonymous=404)
    def send_anonymous_request(self, url, ctx):
        self.send_request(url, ctx, expected_staff=200, expected_lambda=404, expected_anonymous=200)
    def send_request(self, url, ctx, expected_staff=200, expected_lambda=200, expected_anonymous=200):
        self.assertEqual(self.anonymous_client.get(url, ctx).status_code, expected_anonymous, f'Expecting status {expected_anonymous} for url {url} with anonymous')
        self.assertEqual(self.client.get(url, ctx).status_code, expected_lambda, f'Expecting status {expected_lambda} for url {url} with lambda user')
        self.assertEqual(self.staff_client.get(url, ctx).status_code, expected_staff, f'Expecting status {expected_staff} for url {url} with staff user')