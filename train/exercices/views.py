from itertools import permutations
from django.http import Http404, JsonResponse
from django.shortcuts import render

from train.models import Exercice
from django.db.models import Q
from lfainfo22.views import BaseView

from django.core import serializers
from api.views import ApiView
from api.urls import api

import json
import random
import unidecode

from django.conf import settings

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

@api
class GetMarkovView(ApiView):
    VERSION = 1
    APPLICATION = "train/exercices"
    ROUTE = "markov/default"

    def get_call(self, request, *args, **kwargs):
        solution = []

        while len(solution)<500:
            sentence = settings.MARKOVIFY_MODEL.make_sentence()

            for character in sentence:
                if character in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzéàçèùâêôûœ":
                    decoded_char = unidecode.unidecode(character.upper())
                    solution.append(decoded_char)
        
        solution = "".join(solution)

        return JsonResponse({
            "data": solution,
            "status": 200
        })

@register
class MarkovView(ExerciceView):
    def permutations(self):
        permutations = dict()

        for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            j=random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            while j in permutations:
                j=random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        
            permutations[j]=i
        
        return permutations
    def chiffrer(self, letter, permutations):
        return permutations[letter]
    def get_context_data(self, request, *args, **kwargs):
        permutations=self.permutations()
        text_characters = []
        solution = []

        while len(text_characters)<500:
            sentence = settings.MARKOVIFY_MODEL.make_sentence()

            for character in sentence:
                if character in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzéàçèùâêôû":
                    decoded_char = unidecode.unidecode(character.upper())
                    text_characters.append(self.chiffrer(decoded_char, permutations))
                    solution.append(decoded_char)
        
        solution = "".join(solution)

        frequencies = [(char, text_characters.count(char)) for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        frequencies.sort(key=lambda n:-n[1])
        french_frequencies = list("EASINTRLUODCPMVGFBQHXJYZKW")
        return {}
