
from django.urls import path
from django.conf import settings

urlpatterns = ([
    
], "articles", "articles")

from .views import ArticleView

for article_json in settings.ARTICLES_CONF:
    if article_json['view'] == 'ArticleView':
        urlpatterns[0].append(path(article_json['route'], ArticleView(article_json)))
    
