from django.shortcuts import render
from lfainfo22.views import BaseView

class TrainIndexView(BaseView):
    TEMPLATE_NAME = 'train/list/exercice_list.html'

    def get_context_data(self, request, *args, **kwargs):
        ctx = super().get_context_data(request, *args, **kwargs)

        ctx['exercices'] = [
            { 'text':'Text', 'icon': 'home' } for i in range(20)
        ]
        ctx['properties'] = {
            'schedulers': [ 
                {"type":"text", "text":"Révisions de maths"},
                {"type":"text", "text":"Révisions de maths"},
                {"type":"text", "text":"Révisions de maths"},
                {"type":"link", "text":"Nouveau plan", "url": "/train/schedule", "icon": "create"}
            ]
        }

        return ctx
