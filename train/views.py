from sched import scheduler
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from account.models import User
from lfainfo22.views import BaseView, ItemView
from api.urls import api
from api.views import ApiView
from train.models import TimedExercice, TrainingPlan

class TrainIndexView(BaseView):
    TEMPLATE_NAME = 'train/list/exercice_list.html'

    def get_context_data(self, request, *args, **kwargs):
        ctx = super().get_context_data(request, *args, **kwargs)

        schedulers = [
            {"type":"text", "text":"Révisions de maths"} for plan in TrainingPlan.objects.filter(user=request.user)
        ] if request.user.is_authenticated else []
        schedulers.append({"type":"link", "text":"Nouveau plan", "url": "/train/schedule", "icon": "create"})

        ctx['exercices'] = [
            { 'text':'Text', 'icon': 'home' } for i in range(20)
        ]
        ctx['properties'] = {
            'schedulers': schedulers
        }

        return ctx

class TrainSchedulerListView(BaseView):
    TEMPLATE_NAME = 'train/schedulers/list/index.html'

class TrainSchedulerItemView(ItemView):
    TEMPLATE_NAME = 'train/schedulers/item/index.html'

    FILTER_ARGUMENTS = [
        ('URL', 'id', 'id')
    ]
    ITEM_MODEL   = TrainingPlan
    ITEM_CONTEXT = 'scheduler'

#
# API
#

@api
class GetAllTrainingPlans(ApiView):
    VERSION = 1
    APPLICATION = "train"
    ROUTE = "get/plan/all/"

    PAGINATION = 10

    def permission(self, request, *args, **kwargs):
        self.username = '' if request.user.is_anonymous else request.user.username
        if 'related' in request.GET:
            self.username = request.GET['related']
        
        if self.username == '':
            return JsonResponse({
                'data': [],
                'status': 404,
                'error': 'Cannot search for all global training plans'
            })
    
    def get_data(self, training_plan):
        return {
            'id': training_plan.id,
            'name': training_plan.name,
            'exercices': list(map(lambda x: x.id, training_plan.timed_exercices.all()))
        }

    def get_call(self, request, *args, **kwargs):
        if 'last_seen' in request.GET:
            training_plans = TrainingPlan.objects.filter(user__username=self.username, id__lt=int(request.GET['last_seen'])).order_by('-id')[:self.PAGINATION]
        else:
            training_plans = TrainingPlan.objects.filter(user__username=self.username).order_by('-id')[:self.PAGINATION]

        return JsonResponse({
            'data': list(map(self.get_data, training_plans)),
            'status': 200
        })

@api
class GetTimedExercices(ApiView):
    VERSION = 1
    APPLICATION = "train"
    ROUTE = "get/exercice/timed/<int:id>"
    
    def permission(self, request, *args, **kwargs):
        self.obj = get_object_or_404(TimedExercice, id=kwargs['id'])

        return super().permission(request, *args, **kwargs)

    def get_call(self, request, *args, **kwargs):
        return JsonResponse({
            'data': {
                'exercice': self.obj.exercice.name,
                'minutes': self.obj.minutes,
                'seconds': self.obj.seconds,
            },
            'status': 200
        })

@api
class DeleteTrainingPlan(ApiView):
    VERSION = 1
    APPLICATION = "train"
    ROUTE = "delete/scheduler/<int:id>"

    def permission(self, request, *args, **kwargs):
        self.object = get_object_or_404(TrainingPlan, id=kwargs['id'])
        if self.object.user != request.user: raise Http404()

        return super().permission(request, *args, **kwargs)
    
    def get_call(self, request, *args, **kwargs):
        json_resp = False
        if 'json_resp' in request.GET: json_resp = request.GET['json_resp'] in ["True", True, "true"]

        next = '/train/schedule/'
        if 'next' in request.GET: next = request.GET['next']

        self.object.delete()

        if json_resp:
            return JsonResponse({
                "status": 200,
                "data": True,
            })
        
        return redirect(next)