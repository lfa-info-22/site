
from django.urls import path

from train.views import TrainIndexView, TrainSchedulerListView, TrainSchedulerItemView

urlpatterns = ([
    path('', TrainIndexView()),
    path('schedule/', TrainSchedulerListView()),
    path('schedule/<int:id>/', TrainSchedulerItemView())
], "train", "train")
