from django.shortcuts import render
from lfainfo22.views import BaseView

class TrainIndexView(BaseView):
    TEMPLATE_NAME = 'train/list/exercice_list.html'
