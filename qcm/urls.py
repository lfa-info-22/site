
from django.urls import path
from qcm.views   import EditorView

urlpatterns = ([
    path('editor', EditorView()),
], "qcm", "qcm")
