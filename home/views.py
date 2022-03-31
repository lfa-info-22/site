from django.shortcuts import render
from lfainfo22.views  import BaseView
from django.conf      import settings

class HomeView(BaseView):
    TEMPLATE_NAME = 'home/index.html'

class PublicationsView(BaseView):
    TEMPLATE_NAME = 'home/posts.html'

    def get_context_data(self, request, *args, **kwargs):
        ctx = super().get_context_data(request, *args, **kwargs)

        ctx['publications'] = settings.ARTICLES_CONF

        return ctx

