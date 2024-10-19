from functools import wraps 
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import *

def xhr_request_only():
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':   
                return view(request, *args, **kwargs)  
        return wrapper
    return decorator


