from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from lfainfo22.views  import BaseView
from qcm.models       import QCM, QCMQuestion, QCMAnswer, QCMUserResponse
from api.views        import ApiView
from api.urls         import api
import django.utils.timezone as timezone
import math

class QCMHomeView(BaseView):
    TEMPLATE_NAME = "qcm/index.html"
    PAGINATION    = 10

    def get_context_data(self, request, *args, **kwargs):
        ctx = super().get_context_data(request, *args, **kwargs)

        page_count = math.ceil(QCM.objects.count() / self.PAGINATION)

        page = min(page_count - 1, max(0, int(request.GET['page']) if 'page' in request.GET else 0))

        ctx['qcm_array'] = QCM.objects.all()[
             page      * self.PAGINATION 
             : 
            (page + 1) * (self.PAGINATION)
        ]

        ## sort index, warp (False if no link), text
        pages = set([ (-1000, 0, '<<', True, False), (-999, max(0, page - 1), '<', True, False) ])

        for i in range(min(3, page_count)):
            pages.add((i, i, str(i + 1), True, i == page))
        for i in range(max(0, page_count - 3), page_count):
            pages.add((i, i, str(i + 1), True, i == page))
        for i in range(max(0, page - 1), min(page_count, page + 2)):
            pages.add((i, i, str(i + 1), True, i == page))
        
        pages = list(pages)
        pages.sort()

        idx = 2
        while idx < len(pages) - 1:
            if pages[idx][1] + 1 != pages[idx + 1][1]:
                pages.insert(idx + 1, (-1001, False, '...', False, False))
                idx += 1
            idx += 1

        pages.append((-999, min(page_count - 1, page + 1), '>', True, False))
        pages.append((-1000, page_count - 1, '>>', True, False))

        ctx['pages'] = pages

        return ctx

@api
class QCMAnswerView(ApiView):
    VERSION = 1
    APPLICATION = "qcm"
    ROUTE = "answer/set/<int:qcm_id>/<int:question_id>"

    NEEDS_AUTHENTICATION = True
    
    def permission(self, request, *args, **kwargs):
        obj = super().permission(request, *args, **kwargs)
        if obj != None: return obj

        self.qcm      = get_object_or_404(QCM, id=kwargs['qcm_id'])
        self.question = get_object_or_404(self.qcm.questions, id=kwargs['question_id'])

    def get_call(self, request, *args, **kwargs):
        answer, created = QCMUserResponse.objects.get_or_create(user=request.user, question=self.question)
        delta_time = timezone.now() - answer.last_try

        if int(str(delta_time).split(":")[1]) < 3 and answer.try_count >= 3:
            return JsonResponse({  })
        
        answer.try_count += 1
        answer.last_try = timezone.now()
        answer.save()

        return redirect()

class EditorView(BaseView):
    NEEDS_STAFF = True

    TEMPLATE_NAME = "qcm/editor.html"

    def get_context_data(self, request, *args, **kwargs):
        ctx = super().get_context_data(request, *args, **kwargs)

        ctx['qcms'] = QCM.objects.all()

        return ctx
