from sched import scheduler
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from account.models import User
from lfainfo22.views import BaseView, ItemView
from api.urls import api
from api.views import ApiView
from train.models import Exercice, TimedExercice, TrainingPlan
from django.core import serializers

class TrainIndexView(BaseView):
    TEMPLATE_NAME = 'train/list/exercice_list.html'

    def get_context_data(self, request, *args, **kwargs):
        ctx = super().get_context_data(request, *args, **kwargs)

        schedulers = [
            {"type":"text", "text":plan.name, "value": plan.id} for plan in TrainingPlan.objects.filter(user=request.user).order_by("-id")
        ] if request.user.is_authenticated else []
        print(TrainingPlan.objects.all())
        schedulers.append({"type":"link", "text":"Nouveau plan", "url": "/train/schedule?next=/train", "icon": "create"})

        ctx['categories'] = [
            
        ]

        categories = {}
        for exercice in Exercice.objects.all():
            if not exercice.category in categories:
                categories[exercice.category] = len(ctx['categories'])
                ctx['categories'].append({
                    "name": exercice.category,
                    "exercices": []
                })
            
            ctx['categories'][ categories[exercice.category] ]['exercices'].append(exercice)
        
        ctx['properties'] = {
            'schedulers': schedulers
        }

        return ctx

class TrainSchedulerListView(BaseView):
    TEMPLATE_NAME = 'train/schedulers/list/index.html'

    def get_context_data(self, request, *args, **kwargs):
        ctx = super().get_context_data(request, *args, **kwargs)

        ctx['create_next'] = "/train/schedule"
        if 'next' in request.GET:
            ctx['create_next'] = request.GET['next']

        return ctx

class TrainSchedulerItemView(ItemView):
    TEMPLATE_NAME = 'train/schedulers/item/index.html'

    FILTER_ARGUMENTS = [
        ('URL', 'id', 'id')
    ]
    ITEM_MODEL   = TrainingPlan
    ITEM_CONTEXT = 'scheduler'

class TrainExercicePlayerView(ItemView):
    TEMPLATE_NAME = 'train/exercices/player.html'

    FILTER_ARGUMENTS = [
        ('URL', 'id', 'id')
    ]
    ITEM_MODEL   = TrainingPlan
    ITEM_CONTEXT = 'scheduler'

    def get_context_data(self, request, *args, **kwargs):
        ctx = super().get_context_data(request, *args, **kwargs)
        
        ctx['metadata'] = serializers.serialize('json', self._itemview_item.timed_exercices.all())

        return ctx

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
                'count': self.obj.count,
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
class CreateTrainingPlan(ApiView):
    VERSION = 1
    APPLICATION = "train"
    ROUTE = "create/scheduler"

    NEEDS_AUTHENTICATION = True

    def get_call(self, request, *args, **kwargs):
        if not 'name' in request.GET:
            raise Http404()
        
        plan = TrainingPlan.objects.create(user=request.user, name=request.GET['name'])

        json_resp = False
        if 'json_resp' in request.GET: json_resp = request.GET['json_resp'] in ["True", True, "true"]

        next = '/train/schedule/<id>'
        if 'next' in request.GET: next = request.GET['next']
        next = str(plan.id).join(next.split('<id>'))

        if json_resp:
            return JsonResponse({
                "data": plan.id,
                "status": 200
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
            count = self.last_ex.count,
        )
        self.object.timed_exercices.add(self.new_object)

        for idx in range(self.exercices.count() - 1, self.e_id, -1):
            self.exercices[idx].exercice = self.exercices[idx - 1].exercice
            self.exercices[idx].minutes = self.exercices[idx - 1].minutes
            self.exercices[idx].seconds = self.exercices[idx - 1].seconds
            self.exercices[idx].count = self.exercices[idx - 1].count

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
        self.ex0.count, self.ex1.count = self.ex1.count, self.ex0.count

        self.ex0.save()
        self.ex1.save()

        return self.get_return(request)

@api
class ModifyTimedExercice(ApiView):
    VERSION = 1
    APPLICATION = "train"
    ROUTE = "modify/scheduler/<int:s_id>/exercice/<int:e_id>"

    def permission(self, request, *args, **kwargs):
        self.object = get_object_or_404(TrainingPlan, id=kwargs['s_id'])
        if self.object.user != request.user: raise Http404()
        
        self.exercice = get_object_or_404(self.object.timed_exercices, id=kwargs['e_id'])

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
        self.exercice.minutes = int(request.GET['minutes']) if 'minutes' in request.GET else self.exercice.minutes
        self.exercice.seconds = min(59, max(0, int(request.GET['seconds']))) if 'seconds' in request.GET else self.exercice.seconds
        self.exercice.count = int(request.GET['repetitions']) if 'repetitions' in request.GET else self.exercice.count
        self.exercice.save()

        return self.get_return(request)

@api
class CreateTimedExercice(ApiView):
    VERSION = 1
    APPLICATION = "train"
    ROUTE = "create/scheduler/<int:s_id>/exercice/<int:e_id>"

    def permission(self, request, *args, **kwargs):
        self.object = get_object_or_404(TrainingPlan, id=kwargs['s_id'])
        if self.object.user != request.user: raise Http404()
        
        self.exercice = get_object_or_404(Exercice, id=kwargs['e_id'])

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
        self.object.timed_exercices.add(
            TimedExercice.objects.create(exercice=self.exercice, minutes=1, seconds=0, count=1)
        )

        return self.get_return(request)
