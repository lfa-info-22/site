from django.shortcuts import render
from lfainfo22.views  import BaseView
from qcm.models       import QCM, QCMQuestion, QCMAnswer

# Create your views here.
class EditorView(BaseView):
    NEEDS_STAFF = True

    TEMPLATE_NAME = "qcm/editor.html"

    def get_context_data(self, request, *args, **kwargs):
        ctx = super().get_context_data(request, *args, **kwargs)

        ctx['qcms'] = QCM.objects.all()

        return ctx
