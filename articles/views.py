from django.shortcuts import render
from lfainfo22.views  import BaseView

class ArticleView(BaseView):
    def __init__(self, json) -> None:
        super().__init__()
        
        self.TEMPLATE_NAME = json['template']