import logging
from django.http import HttpResponse
from django.shortcuts import redirect
logger = logging.getLogger(__name__)

class AuthMiddlewere(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = request.path
        if 'customer' in request.session: 
            if request.path == '/login/' or request.path == '/register/':
                return redirect('/')
            else:
                return self.get_response(request)

        return self.get_response(request)
