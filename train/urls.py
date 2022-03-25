
from django.urls import path

from train.views import TrainIndexView

urlpatterns = ([
    path('', TrainIndexView())
], "train", "train")
