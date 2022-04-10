
from django.urls import path
from train.exercices.views import ExerciceViewDispatcher

from train.views import TrainIndexView, TrainSchedulerListView, TrainSchedulerItemView, TrainExercicePlayerView

urlpatterns = ([
    path('', TrainIndexView()),
    path('schedule/', TrainSchedulerListView()),
    path('schedule/<int:id>/', TrainSchedulerItemView()),

    path('exercice/data/<str:slug>', ExerciceViewDispatcher()),
    path('exercice/player/<int:id>', TrainExercicePlayerView())
], "train", "train")
