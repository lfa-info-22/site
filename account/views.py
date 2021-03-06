
from django.contrib.auth import authenticate, login, logout
from django.shortcuts    import render, redirect
from account.models      import User
from django.urls         import reverse
from django.http         import JsonResponse
from api.views           import ApiView
from api.urls            import api

from django.shortcuts import render
from lfainfo22.views  import BaseView
from django.conf      import settings

class LoginView(BaseView):
    TEMPLATE_NAME = 'account/login.html'

class CreateAccountView(BaseView):
    TEMPLATE_NAME = "account/signup.html"

'''
Account API Views
'''

@api
class ApiLoginView(ApiView):
    VERSION     = 1
    APPLICATION = 'account'
    ROUTE       = 'login/'

    ALLOWED_METHODS = [ 'POST' ]

    POST_PARAMS = [
        ('user', 'default'), ## Either username or email or both, depending on config
        ('password', 'default'),
    ]

    USERNAME_AUTH = True
    EMAIL_AUTH = True

    LOGIN_REDIRECTOR = 'account:login'
    LOGIN_REDIRECTOR__NEXT_GET_ARG = 'next'

    def authenticate(self, username, password):
        user = authenticate(username=username, password=password) \
               if self.USERNAME_AUTH else None
        
        if user is not None or not self.EMAIL_AUTH: 
            return user

        username_filter = User.objects.filter(email=username)
        if username_filter.count() != 1: 
            return None

        return authenticate(
            username=username_filter[0].username,
            password=password
        )

    def post_call(self, request, *args, **kwargs):
        username = request.POST['user']
        password = request.POST['password']

        redirector = request.GET['next'] if 'next' in request.GET else '/' 
        json_resp  = 'json_resp' in request.GET and request.GET['json_resp'] == 'true'

        user = self.authenticate(username, password)

        if user is not None: login(request, user)

        if json_resp:
            return JsonResponse({ "status": user is not None })
        
        if user is None:
            return redirect(
                reverse( self.LOGIN_REDIRECTOR ) \
                    + '?' + self.LOGIN_REDIRECTOR__NEXT_GET_ARG + '=' \
                    + redirector
            )

        return redirect( redirector )

@api
class ApiLogoutView(ApiView):
    VERSION     = 1
    APPLICATION = "account"
    ROUTE       = "logout/"

    ALLOWED_METHODS = [ 'GET', 'POST' ]

    def post_call(self, request, *args, **kwargs):
        return self.get_call(request, *args, **kwargs)
    def get_call(self, request, *args, **kwargs):
        logout(request)

        redirector = request.GET['next'] if 'next' in request.GET else '/' 
        json_resp  = 'json_resp' in request.GET and request.GET['json_resp'] == 'true'

        if json_resp:
            return JsonResponse({ "status": request.user.is_anonymous })

        return redirect(redirector)
