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

@api
class DuplicateTrainingPlan(ApiView):
    VERSION = 1
    APPLICATION = "train"
    ROUTE = "copy/scheduler/<int:id>"

    NEEDS_AUTHENTICATION = True

    def permission(self, request, *args, **kwargs):
        self.object = get_object_or_404(TrainingPlan, id=kwargs['id'])

        return super().permission(request, *args, **kwargs)

    def get_call(self, request, *args, **kwargs):
        json_resp = False
        if 'json_resp' in request.GET: json_resp = request.GET['json_resp'] in ["True", True, "true"]

        next = '/train/schedule/<id>'
        if 'next' in request.GET: next = request.GET['next']

        self.new_object = TrainingPlan.objects.create(name=self.object.name, user=request.user)

        for timed_exercice in self.object.timed_exercices.all():
            new_exercice = TimedExercice.objects.create(
                exercice = timed_exercice.exercice,
                seconds  = timed_exercice.seconds,
                minutes  = timed_exercice.minutes
            )

            self.new_object.timed_exercices.add(new_exercice)
        
        if json_resp:
            return JsonResponse({
                "status": 200,
                "data": self.new_object.id,
            })
        
        return redirect(next.replace("<id>", str(self.new_object.id)))

@api
class DuplicateTimedExercice(ApiView):
    VERSION = 1
    APPLICATION = "train"
    ROUTE = "copy/scheduler/<int:s_id>/exercice/<int:e_id>"

    def permission(self, request, *args, **kwargs):
        self.object = get_object_or_404(TrainingPlan, id=kwargs['s_id'])
        if self.object.user != request.user: raise Http404()

        self.exercices = self.object.timed_exercices.all()
        self.e_id = 0
        while self.e_id < len(self.exercices) and self.exercices[self.e_id].id != kwargs['e_id']:
            self.e_id += 1
        
        if self.e_id == self.exercices.count():
            raise Http404()

        self.last_ex = self.exercices[self.exercices.count() - 1]

        return super().permission(request, *args, **kwargs)

    def get_call(self, request, *args, **kwargs):
        json_resp = False
        if 'json_resp' in request.GET: json_resp = request.GET['json_resp'] in ["True", True, "true"]

        next = '/train/schedule/<id>'
        if 'next' in request.GET: next = request.GET['next']

        self.new_object = TimedExercice.objects.create(
            exercice = self.last_ex.exercice,
            minutes = self.last_ex.minutes,
            seconds = self.last_ex.seconds,
        )
        self.object.timed_exercices.add(self.new_object)

        for idx in range(self.exercices.count() - 1, self.e_id, -1):
            self.exercices[idx].exercice = self.exercices[idx - 1].exercice
            self.exercices[idx].minutes = self.exercices[idx - 1].minutes
            self.exercices[idx].seconds = self.exercices[idx - 1].seconds

            self.exercices[idx].save()

        if json_resp:
            return JsonResponse({
                "status": 200,
                "data": self.new_object.id,
            })
        
        return redirect(next.replace("<id>", str(self.object.id)))

@api
class DeleteTimedExercice(ApiView):
    VERSION = 1
    APPLICATION = "train"
    ROUTE = "delete/scheduler/<int:s_id>/exercice/<int:e_id>"

    def permission(self, request, *args, **kwargs):
        self.object = get_object_or_404(TrainingPlan, id=kwargs['s_id'])
        if self.object.user != request.user: raise Http404()

        return super().permission(request, *args, **kwargs)

    def get_call(self, request, *args, **kwargs):
        json_resp = False
        if 'json_resp' in request.GET: json_resp = request.GET['json_resp'] in ["True", True, "true"]

        next = '/train/schedule/<id>'
        if 'next' in request.GET: next = request.GET['next']

        self.object.timed_exercices.filter(id=kwargs['e_id']).delete()

        if json_resp:
            return JsonResponse({
                "status": 200,
                "data": True,
            })
        
        return redirect(next.replace("<id>", str(self.object.id)))

@api
class SwapTimedExercice(ApiView):
    VERSION = 1
    APPLICATION = "train"
    ROUTE = "swap/scheduler/<int:s_id>/exercice/<int:e_id>/<str:direction>"

    def permission(self, request, *args, **kwargs):
        no_throw = request.GET['no_throw'] in ['True', True, 'true'] if 'no_throw' in request.GET else False

        self.object = get_object_or_404(TrainingPlan, id=kwargs['s_id'])
        if self.object.user != request.user: raise Http404()

        self.exercices = self.object.timed_exercices.all()
        self.e_id = 0
        while self.e_id < len(self.exercices) and self.exercices[self.e_id].id != kwargs['e_id']:
            self.e_id += 1
        self.second_e_id = int(kwargs['direction']) + self.e_id

        if not (0 <= self.e_id < len(self.exercices)): 
            if no_throw: return self.get_return(request)
            raise Http404()
        if not (0 <= self.second_e_id < len(self.exercices)):
            if no_throw: return self.get_return(request)
            raise Http404()

        return super().permission(request, *args, **kwargs)
    
    def get_return(self, request):
        json_resp = False
        if 'json_resp' in request.GET: json_resp = request.GET['json_resp'] in ["True", True, "true"]

        next = '/train/schedule/<id>'
        if 'next' in request.GET: next = request.GET['next']

        if json_resp:
            return JsonResponse({
                "status": 200,
                "data": True,
            })
        
        return redirect(next.replace("<id>", str(self.object.id)))

    def get_call(self, request, *args, **kwargs):
        self.ex0 = self.exercices[self.e_id]
        self.ex1 = self.exercices[self.second_e_id]

        self.ex0.exercice, self.ex1.exercice = self.ex1.exercice, self.ex0.exercice
        self.ex0.minutes, self.ex1.minutes = self.ex1.minutes, self.ex0.minutes
        self.ex0.seconds, self.ex1.seconds = self.ex1.seconds, self.ex0.seconds

        self.ex0.save()
        self.ex1.save()

        return self.get_return(request)
