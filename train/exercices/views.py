from django.http import Http404, JsonResponse
from django.shortcuts import render

from train.models import Exercice
from django.db.models import Q
from lfainfo22.views import BaseView

from django.core import serializers

import json

REGISTERED_EXERCICE_VIEWS = {

}
def register (cls):
    REGISTERED_EXERCICE_VIEWS[cls.__name__] = cls
    return cls

class ExerciceView(BaseView):
    def __init__(self, exercice) -> None:
        super().__init__()

        self.exercice = exercice
    
    def get_call(self, request, *args, **kwargs):
        return render(request, self.exercice.template, self.get_context_data(request, *args, **kwargs))

class ExerciceViewDispatcher:
    def __call__(self, request, *args, **kwargs):
        slug_id = 0
        try:
            slug_id = int(kwargs['slug'])
        except Exception:
            pass

        exercice = Exercice.objects.filter(Q(name=kwargs['slug']) | Q(slug=kwargs['slug']) | Q(id=slug_id))
        if len(exercice) == 0: raise Http404()

        if 'metadata' in request.GET:
            return JsonResponse({
                "status": 200,
                "data": json.loads(serializers.serialize('json', exercice))[0]['fields']
            })

        exercice = exercice[0]
        if exercice.view.lower() in ['none', 'null']: raise Http404()
        if exercice.view.lower() in ['default']:
            return ExerciceView(exercice)(request, *args, **kwargs)
        
        return REGISTERED_EXERCICE_VIEWS[exercice.view](exercice)(request, *args, **kwargs)

@register
class TestExerciceView(ExerciceView):
    pass
