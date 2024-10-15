from functools import wraps 
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import *

def permission_required():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            
            url = request.path.split('/')
            filterUrl = url[1:4]
            access = "/".join(filterUrl)
            
            userGroupIds = list(request.user.groups.values_list('id', flat=True))
            # kwargs['allows'] = list(UserAllow.objects.filter(group__in=userGroupIds).values_list('allow', flat=True))
            groupList=[]
            kwargs['moduleIds'] = []
            kwargs['permission'] = []
            if 1 in userGroupIds:
                module_id = Module.objects.filter(url=access).values_list('id', flat=True).first()
                permission = ModuleAction.objects.filter(module_id=module_id).values_list('permission', flat=True).first()
                print(module_id)
                if permission:
                    kwargs['moduleIds'] = Module.objects.values_list('id',flat=True)
                    kwargs['permission'] = permission.split(",")
                    
                    kwargs['groupIds'] = Group.objects.values_list('id', flat=True)
            else:
                groupList = GroupPermission.objects.filter(group__in=userGroupIds,permission__icontains='View').all()
                kwargs['groupIds'] = userGroupIds
                
                for item in groupList:
                    kwargs['moduleIds'].append(item.module_id)
                    
                    if access==item.module.url:
                        access = item.permission.split(",")
                        kwargs['permission'].extend(access)
            
            
            return view(request, *args, **kwargs) 
   
             
            if request.META.get('HTTP_REFERER') == None:
               return redirect("redirect")
            else:
                return redirect(request.META.get('HTTP_REFERER'))
        return _wrapped_view
    return decorator


def xhr_request_only():
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                url = request.path.split('/')
                filterUrl = url[1:4]
                access = "/".join(filterUrl)
                userGroupIds = list(request.user.groups.values_list('id', flat=True))
                # kwargs['allows'] = list(UserAllow.objects.filter(group__in=userGroupIds).values_list('allow', flat=True))
                
                groupList=[]
                kwargs['moduleIds'] = []
                kwargs['permission'] = []
                if 1 in userGroupIds:
                    module_id = Module.objects.filter(url=access).values_list('id', flat=True).first()
                    permission = ModuleAction.objects.filter(module_id=module_id).values_list('permission', flat=True).first()
                    kwargs['moduleIds'] = Module.objects.values_list('id',flat=True)
                    access = permission if permission else 'View'
                    kwargs['permission'] = access.split(",")
                    kwargs['groupIds'] = Group.objects.values_list('id', flat=True)
                else:
                    groupList = GroupPermission.objects.filter(group__in=userGroupIds,permission__icontains='View').all()
                    kwargs['groupIds'] = userGroupIds
                    for item in groupList:
                        kwargs['moduleIds'].append(item.module_id)
                        if access==item.module.url:
                            access = item.permission.split(",")
                            kwargs['permission'].extend(access)
                     
                return view(request, *args, **kwargs)  
        return wrapper
    return decorator


