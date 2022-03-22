
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.html import escape
from django.utils import translation
import re

class BaseView():
    #
    # Utils
    #
    def make_string_safe(self, string):
        return '<br>'.join(escape(string).split('\n'))

    #
    # Permissions
    #

    NEEDS_ANONYMOUS = False
    NEEDS_AUTHENTICATION = False
    NEEDS_STAFF = False

    ALLOWED_METHODS = [ 'GET' ]

    URL_PARAMS = [ ]
    GET_PARAMS = [ ]
    POST_PARAMS = [
        # ('needed', 'default') -> field needed of validation type default
        # ('needed', 'email') -> field needed of validation type email
        # ('?not_needed', type) -> optionnal field
    ]
    
    EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    ## Raise Http error or return redirect / render
    def raise_permission_error(self):
        raise Http404()
    def raise_method_error(self):
        raise Http404()
    def raise_parameter_error(self, type='GET'):
        raise Http404()

    def validate_mail(self, mail):
        return re.fullmatch(self.EMAIL_REGEX, mail)
    def permission(self, request, *args, **kwargs):
        redirector = None

        ## If the user is staff member, display page anyway
        if not request.user.is_staff:
            if self.NEEDS_STAFF:
                redirector = self.raise_permission_error()
            if self.NEEDS_ANONYMOUS and request.user.is_authenticated:
                redirector = self.raise_permission_error()
            if self.NEEDS_AUTHENTICATION and request.user.is_anonymous:
                redirector = self.raise_permission_error()
            if redirector != None: return redirector

        if not request.method in self.ALLOWED_METHODS:
            redirector = self.raise_method_error()
        if redirector != None: return redirector
        
        for url_param in self.URL_PARAMS:
            if not url_param in kwargs:
                redirector = self.raise_parameter_error('URL')

        if request.method == 'GET':
            for get_param in self.GET_PARAMS:
                if not get_param in request.GET:
                    redirector = self.raise_parameter_error('GET')
        
        if request.method == 'POST':
            for post_param, validation_type in self.POST_PARAMS:
                needed = True
                if len(post_param) != 0 and post_param[0] == '?':
                    needed = False
                    post_param = post_param[1:len(post_param)]
                if not post_param in request.POST:
                    if needed:
                        redirector = self.raise_parameter_error('POST')
                else:
                    if validation_type == 'email':
                        if not self.validate_mail(request.POST[post_param]):
                            redirector = self.raise_parameter_error('POST')

        if redirector != None: return redirector
        
        return redirector

    #
    # Get method
    #
    TEMPLATE_NAME = ''

    def get_context_data(self, request, *args, **kwargs):
        return {}
    def get_call(self, request, *args, **kwargs):
        translation.activate(request.session[translation.LANGUAGE_SESSION_KEY] if translation.LANGUAGE_SESSION_KEY in request.session else 'fr')
        return render(request, self.TEMPLATE_NAME, self.get_context_data(request, *args, **kwargs))

    #
    # Post method
    #
    def post_call(self, request, *args, **kwargs):
        return

    def __call__(self, request, *args, **kwargs):
        if (redirector := self.permission(request, *args, **kwargs)) != None:
            return redirector
        
        if request.method == 'GET':
            return self.get_call(request, *args, **kwargs)
        if request.method == 'POST':
            return self.post_call(request, *args, **kwargs)



class ItemView(BaseView):
    #
    # Object to get
    #
    FILTER_ARGUMENTS = [
        ('URL', 'id', 'id')
    ]
    ITEM_MODEL = None
    ITEM_CONTEXT = ''

    def raise_item_error(self):
        raise Http404()
    def permission(self, request, *args, **kwargs):
        redirector = super().permission(request, *args, **kwargs)
        if redirector != None: return redirector

        filters = {}
        for f_type, name, filter_name in self.FILTER_ARGUMENTS:
            if f_type == 'URL':
                filters[filter_name] = kwargs[name]
            if f_type == 'GET':
                filters[filter_name] = request.GET[name]
            if f_type == 'POST':
                filters[filter_name] = request.POST[name]
            if f_type == 'CONST':
                filters[filter_name] = name
        
        try:
            self._itemview_item = self.ITEM_MODEL.objects.get(**filters)
        except Exception as exception:
            redirector = self.raise_item_error()
        return redirector
    
    def get_context_data(self, request, *args, **kwargs):
        ctx = super().get_context_data(request, *args, **kwargs)
        ctx[self.ITEM_CONTEXT] = self._itemview_item
        return ctx


class ListView(BaseView):
    #
    # Objects to get
    #
    FILTER_ARGUMENTS = [
        ('URL', 'id', 'id')
    ]
    ITEM_MODEL = None
    ITEM_CONTEXT = ''

    def raise_item_error(self):
        raise Http404()
    def permission(self, request, *args, **kwargs):
        redirector = super().permission(request, *args, **kwargs)
        if redirector != None: return redirector

        filters = {}
        for f_type, name, filter_name in self.FILTER_ARGUMENTS:
            if f_type == 'URL':
                filters[filter_name] = kwargs[name]
            if f_type == 'GET':
                filters[filter_name] = request.GET[name]
            if f_type == 'POST':
                filters[filter_name] = request.POST[name]
            if f_type == 'CONST':
                filters[filter_name] = name

        try:
            self._listview_item = self.ITEM_MODEL.objects.filter(**filters)
        except Exception as exception:
            redirector = self.raise_item_error()
        return redirector
    
    def get_context_data(self, request, *args, **kwargs):
        ctx = super().get_context_data(request, *args, **kwargs)
        ctx[self.ITEM_CONTEXT] = self._listview_item
        return ctx

