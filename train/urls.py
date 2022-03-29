
from django.urls import path

from train.views import TrainIndexView, TrainSchedulersView

urlpatterns = ([
    path('', TrainIndexView()),
    path('schedule/', TrainSchedulersView())
], "train", "train")
