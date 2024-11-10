import logging
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
logger = logging.getLogger(__name__)

class AuthMiddlewere(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = request.path
        if request.user.is_authenticated:
            if request.path == '/admin/login/' or request.path == '/admin/register/':
                return redirect(settings.BASE_URL+'admin/dashboard/')
            else:
                return self.get_response(request)
        else:
            if request.path == '/admin/dashboard/':
               return redirect(settings.BASE_URL+'admin/login/')
            else:
               return self.get_response(request)
