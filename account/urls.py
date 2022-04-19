from account.views import CreateAccountView, LoginView
from django.urls import path

urlpatterns = ([
    path('login/', LoginView(), name='login'),
    path('create/', CreateAccountView(), name='create')
], "account", "account")

