
from django.urls import path
from qcm.views   import EditorView, QCMHomeView

urlpatterns = ([
    ## User  area
    path('', QCMHomeView()),

    ## Admin area
    path('editor', EditorView()),
], "qcm", "qcm")
