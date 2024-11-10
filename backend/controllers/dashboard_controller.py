from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import Group, Permission,ContentType
from django import forms
from django.db.models import Q
from django.conf import settings
from backend.models import *
from frontend.models import *
import json
from backend.decorators import (
   permission_required,
   xhr_request_only,
   # add_edit_permission
)



def dashboard(request):
    return render(request,"admin/dashboard.html")

@permission_required()
def permission(request,*args,**kwargs):
   if request.method == 'POST':
      listData = []
      totalLen=0
      if 'View' in kwargs.get('permission'):
         start = request.POST['start']
         length = request.POST['length']
         search = request.POST['search']
         startIndex = (int(start)-1) * int(length)
         endIndex = startIndex + int(length)
         
         allowed = list(UserAllow.objects.filter(group__in=kwargs.get('groupIds')).values_list('allow', flat=True))
         permission = allowed[0].split(",") if allowed else []
         if search :
            data = Group.objects.filter(name__contains=search,id__in=permission)[startIndex:endIndex].all()
            totalLen = Group.objects.filter(name__contains=search,id__in=permission).count()
            
         else:
            data = Group.objects.filter(id__in=permission)[startIndex:endIndex].all()
            totalLen = Group.objects.filter(id__in=permission).count()

        
         for i in data:
               
               permission = {
               "id":i.id,
               "roleName":i.name,
               "action":f'<a class="btn btn-primary" href="{settings.BASE_URL}admin/administration/permission/{i.id}" >Permission</a>'
                        # f'<a class="btn btn-danger" href="{settings.BASE_URL}admin/administration/permission/{i.id}/delete" >Delete</a>'
               }

               listData.append(permission)
      
         
      return JsonResponse({
         "success": True,
         "iTotalRecords":totalLen,
         "iTotalDisplayRecords":totalLen,
         "aaData":listData
      }, status=200)
   
      # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:
      return render(request,"admin/administration/index.html")

@permission_required()
def deletePermission(request,*args,**kwargs):
    if 'Delete' in kwargs.get('permission'):
        groupId = kwargs.get('roleId')
        Group.objects.filter(id=groupId).delete()
        GroupAllow.objects.filter(group_id=groupId,user=request.user).delete()          
    return HttpResponseRedirect(request.META['HTTP_REFERER'])    

@xhr_request_only()
def addEditPermission(request,*args,**kwargs):
    groupIds = kwargs.get('groupIds')
    if 'Add' in kwargs.get('permission'):
      if request.method == 'POST':
         post = request.POST
         group = Group.objects.create(
            name=post['group']             
         )
         allow = UserAllow.objects.filter(group_id__in=kwargs.get('userGroup'))
         if allow.exists():
            for i in allow:
               grp = str(group.id)
               if grp not in i.allow:
                  allow = i.allow
                  i.allow = allow +","+ str(group.id)
                  i.save()
         else:
            grpId = ",".join(map(str, kwargs.get('userGroup')))
            UserAllow.objects.create(
               allow=group.id,
               group=Group.objects.get(id=grpId)
            )
      return JsonResponse({
         "success": True,
         "status":"Successfully added!",
      }, status=200)   
    else:
         return JsonResponse({
            "success": False,
            "access":"You don't have add permission!"
         }, status=200) 

@permission_required()
def rolePermission(request,*args,**kwargs):
    roleId = kwargs.get('roleId')
    parentId = kwargs.get('parentId', '')
    
    if request.method == 'POST':
      listData = []
      totalLen=0
      
      if set(['View']).issubset(kwargs.get('permission')):
         start = int(request.POST['start'])
         length = int(request.POST['length'])
         search = request.POST['search']
         startIndex = (int(start)-1) * int(length)
         endIndex = startIndex + int(length)
         moduleIds = kwargs.get('moduleIds')
         groupIds = kwargs.get('groupIds')
         
         if search :
            data =  Module.objects.filter(module__contains=search,id__in=moduleIds).filter(Q(parent_id=parentId))[startIndex:endIndex].all()
            totalLen = Module.objects.filter(module__contains=search,id__in=moduleIds).filter(Q(parent_id=parentId)).count()
         else:
            data =  Module.objects.filter(id__in=moduleIds).filter(Q(parent_id=parentId))[startIndex:endIndex].all()
            totalLen = Module.objects.filter(id__in=moduleIds).filter(Q(parent_id=parentId)).count()

         lst = {}
         # allowed = GroupPermission.objects.filter(group=roleId).values('module','module_parent_id')

         for i in data:
            access_list = list(i.grouppermissions.filter(group=roleId).values_list('permission',flat=True))
            
            if len(access_list):
               access_list= access_list[0].split(",")
            per = f'<div class="d-flex">' 
            if 1 in groupIds:
               allow = ModuleAction.objects.filter(module_id=i.id).filter(Q(module_parent_id=i.parent_id)).all()
            else:
               allow = i.grouppermissions.filter(module_id=i.id,group_id__in=groupIds).filter(Q(module_parent_id=i.parent_id)).all()
            
            per +=f'<input type="hidden" name="permission[{i.id}][{i.parent_id}]" value="">'
            for b in allow:
               # per +=f'<input type="hidden" name="permission[{b.module_id}][{b.module_parent_id}]" value="">'
               for c in b.permission.split(","):
                  checked = 'checked' if c in access_list else ''
                  per +=f'''
                           <div class="form-check px-3">
                              <input class="form-check-input" {checked} name="permission[{b.module_id}][{b.module_parent_id}]" type="checkbox" value="{c}" id="flexCheck{b.id}">
                              <label class="form-check-label" for="flexCheck{b.id}">{c}</label>     
                           </div>
                        '''

            per +='</div>'
            permission = {
               "id":i.id,
               "moduleName":f'<a href="{settings.BASE_URL}admin/administration/permission/{roleId}/{i.id}">{i.module}</a>',
               "permission":per,
               "action":f'''
                           <div class="form-check">
                           <input class="form-check-input" type="checkbox" value="" >
                           <label class="form-check-label" > All</label>
                           </div>
                        '''
            }
         
            listData.append(permission)
                      
      return JsonResponse({
         "success": True,
         "iTotalRecords":totalLen,
         "iTotalDisplayRecords":totalLen,
         "aaData":listData
      }, status=200)
    else:
      context = {
         "roleId":roleId,
         "parentId":parentId
      }
      return render(request,"admin/permission/access.html",context)

@permission_required()  
def savePermission(request,*args,**kwargs):
    roleId = kwargs.get('roleId')
    
    if request.method == 'POST':
      moduleIds = kwargs.get('moduleIds')
      groupIds = kwargs.get('groupIds')
      moduleList =  Module.objects.filter(id__in=moduleIds).all()
      remove = {}
      
      if set(['Edit']).issubset(kwargs.get('permission')):

         for i in moduleList:
            if 1 in groupIds:
               permission = ModuleAction.objects.filter(module_id=i.id).filter(Q(module_parent_id=i.parent_id)).values('module','module_parent_id','permission')
            else:
               # permission = i.grouppermissions.objects.values('module','module_parent_id','permission')
               permission = GroupPermission.objects.filter(module_id=i.id).filter(Q(module_parent_id=i.parent_id)).values('module','module_parent_id','permission')
            
            for b in permission:
               mid = b['module']
               mpid = b['module_parent_id']
               key = f'permission[{mid}][{mpid}]'
               if key in request.POST:
                  if mid not in remove:
                     remove[mid]={'module_id':mid,'module_parent_id':mpid,'permission':request.POST.getlist(key)}
         
 
         for item in remove:
            if len(remove[item]):
               mld = remove[item]           
               GroupPermission.objects.filter(group=roleId,module=mld['module_id']).filter(Q(module_parent_id=mld['module_parent_id'])).delete()
               access_list = [item for item in mld['permission'] if item]
               if len(access_list):
                  access_str = ','.join(access_list)
                  GroupPermission.objects.create(
                     permission=access_str,                  
                     module_id=mld['module_id'],                  
                     module_parent_id=mld['module_parent_id'],
                     group_id=roleId
                  )
      
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@permission_required()
def module(request,*args,**kwargs):
   parentId = kwargs.get('parentId', '')
   if request.method == 'POST':
      start = request.POST['start']
      length = request.POST['length']
      search = request.POST['search']
      startIndex = (int(start)-1) * int(length)
      endIndex = startIndex + int(length)
      moduleIds = kwargs.get('moduleIds')
      listData = []
      totalLen=0
      
      if 'View' in kwargs.get('permission'):
         if search :
            data = Module.objects.filter(Q(parent_id=parentId),id__in=moduleIds,module__contains=search)[startIndex:endIndex].all()
            totalLen = Module.objects.filter(Q(parent_id=parentId),id__in=moduleIds,module__contains=search).count()
         else:
            data = Module.objects.filter(Q(parent_id=parentId),id__in=moduleIds)[startIndex:endIndex].all()
            totalLen = Module.objects.filter(Q(parent_id=parentId),id__in=moduleIds).count()
         
         for i in data:
            if i.moduleType=='1':
               module = f'<a href="{settings.BASE_URL}admin/administration/module/{i.id}">{i.module}</a>'
            else:
               module = i.module
            permission = {
               "id":i.id,
               "module":module,
               # "action":(f'<a href="{settings.BASE_URL}admin/administration/module/{i.id}/delete" class="btn btn-sm btn-danger" >Delete</a>')
            }  
            listData.append(permission)
      
      return JsonResponse({
         "success": True,
         "iTotalRecords":totalLen,
         "iTotalDisplayRecords":totalLen,
         "aaData":listData
      }, status=200)
     
   else:
      context = {
         'parentId':parentId
      }
      return render(request,"admin/administration/module.html",context)

@permission_required()
def deleteModule(request,*args,**kwargs):
    moduleId = kwargs.get('moduleId')
    groupIds = kwargs.get('groupIds')
    if 'Delete' in kwargs.get('permission'):
        GroupPermission.objects.filter(module_id=moduleId,group_id=groupIds[0]).delete()
        ModuleAction.objects.filter(module_id=moduleId).delete()
        Module.objects.filter(id=moduleId).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
      
@xhr_request_only()
def addEditModule(request,*args,**kwargs):
    parentId = kwargs.get('parentId', '')
    groupIds = kwargs.get('groupIds')
    
    if 'Add' in kwargs.get('permission'):
      if request.method == 'POST':
         post = request.POST
         permission = 'View'
         url = ''
         if post['moduleType']==1:
            permission = 'View,Add,Edit,Delete'
            url = post['url']

         else:
            module = Module.objects.create(
                  module=post['module'],
                  moduleType=post['moduleType'],
                  url=url,
                  status='1',
                  parent_id=post['parent_id']
            )
            action = ModuleAction.objects.create(
                  permission=permission,                  
                  module_id=module.id,                  
                  module_parent_id=parentId,
            )
            
            GroupPermission.objects.create(
               permission=permission,                  
               module_id=module.id,                  
               module_parent_id=parentId,
               group_id=groupIds[0]                   
            )

      return JsonResponse({
         "success": True,
         "parentId":parentId,
         "status":"Successfully added!",
      }, status=200)   
    else:
         return JsonResponse({
            "success": False,
            "access":"You don't have add permission!"
         }, status=200)   

@permission_required() 
def user(request,*args,**kwargs):
   if request.method == 'POST':
      listData = []
      totalLen=0
      if set(['View']).issubset(kwargs.get('permission')):
         start = request.POST['start']
         length = request.POST['length']
         search = request.POST['search']
         startIndex = (int(start)-1) * int(length)
         endIndex = startIndex + int(length)
         
         allowed = list(UserAllow.objects.filter(group__in=kwargs.get('groupIds')).values_list('allow', flat=True))
         permission = allowed[0].split(",") if allowed else []

         if search :
            data = Group.objects.filter(name__contains=search,id__in=permission)[startIndex:endIndex].all()
            totalLen = Group.objects.filter(name__contains=search,id__in=permission).count()
            
         else:
            data = Group.objects.filter(id__in=permission)[startIndex:endIndex].all()
            totalLen = Group.objects.filter(id__in=permission).count()


         for i in data:
               # print(i.groups.filter(id__in=permission).all())
               users = i.user_set.all()
               for v in users:
                  user = {
                  "id":v.id,
                  "user":v.first_name,
                  "group":i.name,
                  "action":f'<button class="btn btn-primary mx-1" onclick=addEditModel("GET","",{v.id})  >Edit</button>'
                           f'<a class="btn btn-danger mx-1" href="{settings.BASE_URL}admin/administration/user/{v.id}" >Delete</a>'
                  }
                  listData.append(user)
      
      return JsonResponse({
         "success": True,
         "iTotalRecords":totalLen,
         "iTotalDisplayRecords":totalLen,
         "aaData":listData
      }, status=200)

      # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:
      return render(request,"admin/administration/user.html")

@permission_required() 
def addEditUser(request,*args,**kwargs):
   allowed = list(UserAllow.objects.filter(group__in=kwargs.get('groupIds')).values_list('allow', flat=True))
   permission = allowed[0].split(",") if allowed else []
   if request.method == 'POST' and set(['Edit']).issubset(kwargs.get('permission')):
      post = request.POST
      user = User.objects.get(id=post['user'])
      user.first_name = post['username']
      user.save()
      return JsonResponse({
         "success": True,
         "msg":"Update Successfully!"
      }, status=200)   
   else:
      context = {
         "status":False,
         "msg":"Not have edit permission!"
      }
      if set(['Edit']).issubset(kwargs.get('permission')):
         user = list(User.objects.filter(id=kwargs.get('userId')).values())
         group = list(Group.objects.filter(id__in=permission).values())
         context['status'] = True
         context['user'] = user
         context['group'] = group
         # context['allow'] = permission
         context['msg'] = "Successfully!"

      return JsonResponse(context, status=200)   


@xhr_request_only()
def sidebarList(request,*args,**kwargs):
   moduleIds = kwargs.get('moduleIds')
   sidebarList =  list(Module.objects.filter(id__in=moduleIds).values())
   return JsonResponse({
      "success": True,
      "data":sidebarList
   }, status=200)   
   
 



  
