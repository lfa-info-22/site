from django.shortcuts import render
from lfainfo22.views import BaseView

class ApiView(BaseView):
    VERSION = 1
    APPLICATION = "api"
    ROUTE = ""
