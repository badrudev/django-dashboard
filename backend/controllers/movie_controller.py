from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django import forms
from backend.forms import MovieForm
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
 


@permission_required()
def movieList(request,*args,**kwargs):
   
    if request.method == 'POST':
         start = int(request.POST['start'])
         length = int(request.POST['length'])
         search = request.POST['search']
         startIndex = (int(start)-1) * int(length)
         endIndex = startIndex + int(length)
         moduleIds = kwargs.get('moduleIds')
         groupIds = kwargs.get('groupIds')
         listData = []
         totalLen = 0
         
         if search :
            data =  Posts.objects.filter(name__contains=search)[startIndex:endIndex].all()
            totalLen = Posts.objects.filter(name__contains=search).count()
         else:
            data =  Posts.objects.filter(name__contains=search)[startIndex:endIndex].all()
            totalLen = Posts.objects.filter(name__contains=search).count()

      
         for i in data:
            objects = {
               "id":i.id,
               "name":i.name,
               "rate":i.rate,
               "action":f"<a class='btn btn-sm btn-info mx-1' href='{settings.BASE_URL}admin/movie/post/{i.id}/edit'>Edit</a>"
                        f"<a class='btn btn-sm btn-primary mx-1' href='{settings.BASE_URL}admin/movie/post/{i.id}/delete'>Delete</a>"
            }
            listData.append(objects)

         return JsonResponse({
            "success": True,
            "iTotalRecords":totalLen,
            "iTotalDisplayRecords":totalLen ,
            "aaData":listData
         }, status=200)
        
    else:
         return render(request,"admin/movie/index.html",{})

@permission_required()
def movieEdit(request,*args,**kwargs):
   postId = kwargs.get('postId')
   if 'Edit' in kwargs.get('permission'):
      movie = Posts.objects.filter(id=postId).first()
      if request.method == 'POST':
         post = request.POST
         movie.name = post['name']
         movie.image = post['image']
         movie.rate = post['rate']
         movie.size = post['size']
         movie.genre = post['genre']
         movie.lang = post['lang']
         if 'status' in post:
            movie.status = post['status']
         movie.story = post['story']
         movie.save()
           
      context = {
         'movie':movie,
         'postId':postId,
         'action':f'{settings.BASE_URL}admin/movie/post/{postId}/edit'
      }   
      return render(request,"admin/movie/addEdit.html",context)
   else:
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  
@permission_required()
def movieAdd(request,*args,**kwargs):
   if 'Add' in kwargs.get('permission'):
      form = None
      
      if request.method == 'POST':         
         post = request.POST
         form = MovieForm(post)
         if form.is_valid():
            check = Posts.objects.filter(name=post['name']).first()
            if check==None:
               pass

      context = {
         'action':f'{settings.BASE_URL}admin/movie/post/add',
         'form':form
      }
      return render(request,"admin/movie/addEdit.html",context)
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@permission_required()
def movieDelete(request,*args,**kwargs):
   if 'Delete' in kwargs.get('permission'):
      postId = kwargs.get('postId')
      Posts.objects.filter(id=postId).delete()
   
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Menu list
@permission_required()
def menuList(request,*args,**kwargs):
    parentId = kwargs.get('parentId', '')
    if request.method == 'POST':
      if 'View' in kwargs.get('permission'):
         start = int(request.POST['start'])
         length = int(request.POST['length'])
         search = request.POST['search']
         startIndex = (int(start)-1) * int(length)
         endIndex = startIndex + int(length)
         moduleIds = kwargs.get('moduleIds')
         groupIds = kwargs.get('groupIds')
         listData = []
         totalLen = 0 
         if search :
            data =  Menu.objects.filter(Q(menuId=parentId),name__contains=search)[startIndex:endIndex].all()
            totalLen = Menu.objects.filter(Q(menuId=parentId),name__contains=search).count()
         else:
            data =  Menu.objects.filter(Q(menuId=parentId),name__contains=search)[startIndex:endIndex].all()
            totalLen = Menu.objects.filter(Q(menuId=parentId),name__contains=search).count()

         for i in data:
            objects = {
               "id":i.id,
               "name":f"<a href='{settings.BASE_URL}admin/movie/menu/{i.id}'>{i.name}</a>",
               "action":f"<button class='btn btn-sm btn-info mx-1' onclick=editModel('GET',{i.id})>Edit</button>"
                        # f"<a class='btn btn-sm btn-primary mx-1' href='{settings.BASE_URL}admin/movie/menu/{i.id}/delete'>Delete</a>"
            }
            listData.append(objects)

         return JsonResponse({
            "success": True,
            "iTotalRecords":totalLen,
            "iTotalDisplayRecords":totalLen ,
            "aaData":listData
         }, status=200)
      
    else:
      context = {
         'parentId':parentId
      }
      return render(request,"admin/movie/menu.html",context)

@permission_required()
def menuAdd(request,*args,**kwargs):
    parentId = kwargs.get('parentId', '')
    groupIds = kwargs.get('groupIds')
    
    if 'Add' in kwargs.get('permission'):
      if request.method == 'POST':
         post = request.POST
         if 'id' in post and 'Edit' in kwargs.get('permission'):
            menu = Menu.objects.get(id=post['id'])
            menu.name = post['menu']
            menu.status = post.get('status', 0) 
            menu.save()
         else:
            menu = Menu.objects.create(
               name=post['menu'],
               menuId=post['menuid'],
               status='1',
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
def menuEdit(request,*args,**kwargs):
    menuId = kwargs.get('menuId', '')
    if 'Edit' in kwargs.get('permission'):
         menu = Menu.objects.get(id=menuId)
         return JsonResponse({
            "success": True,
            "name":menu.name,
            "menuId":menu.id,
            "status":menu.status
         }, status=200)   
    else:
         return JsonResponse({
            "success": False,
            "access":"You don't have add permission!"
         }, status=200) 

@permission_required()
def menuDelete(request,*args,**kwargs):
   if 'Delete' in kwargs.get('permission'):
      menuId = kwargs.get('menuId')
      Menu.objects.filter(id=menuId).delete()
   
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       

    
def redirect(request):
    return render(request,"index.html")


def chat(request, *args, **kwargs):
    context = {}
    return render(request, "admin/socket/chat.html", context)





  
