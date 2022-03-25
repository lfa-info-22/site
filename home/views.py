from django.shortcuts import render
from lfainfo22.views  import BaseView

class HomeView(BaseView):
    TEMPLATE_NAME = 'home/index.html'

class PublicationsView(BaseView):
    TEMPLATE_NAME = 'home/posts.html'

