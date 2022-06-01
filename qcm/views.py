from django.shortcuts import render
from lfainfo22.views  import BaseView
from qcm.models       import QCM, QCMQuestion, QCMAnswer
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

# Create your views here.
class EditorView(BaseView):
    NEEDS_STAFF = True

    TEMPLATE_NAME = "qcm/editor.html"

    def get_context_data(self, request, *args, **kwargs):
        ctx = super().get_context_data(request, *args, **kwargs)

        ctx['qcms'] = QCM.objects.all()

        return ctx
