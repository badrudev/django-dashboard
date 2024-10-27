from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from frontend.models import *
from django.db.models import Q
from django.conf import settings
from .forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth import authenticate, login,logout
from backend.decorators import (
   xhr_request_only
)

def home(request):
    if request.method == 'POST':
      action = request.POST['type']
      if action == 'View':
         start = request.POST['start']
         length = request.POST['length']
         search = request.POST['search']
         startIndex = (int(start)-1) * int(length)
         endIndex = startIndex + int(length)
        
        
         if search :
            data = Posts.objects.filter(name__contains=search,status=1)[startIndex:endIndex].all()
            totalLen = Posts.objects.filter(name__contains=search,status=1).count()
           
         else:
            data = Posts.objects.filter(status=1).all()[startIndex:endIndex]
            totalLen = Posts.objects.filter(status=1).count()
        
         listData = []
         for i in data:
            
            post = {
               "id":i.id,
               "name":i.name,
               "image":i.image,
               "rate":i.rate,
              
            }
                
            listData.append(post)
        
         return JsonResponse({
            "success": True,
            "iTotalRecords":totalLen,
            "iTotalDisplayRecords":totalLen,
            "aaData":listData
         }, status=200)
    else:
      trands = Trand.objects.all()[0:4]
      # if 'customer' in request.session:
      #    auth = request.session['customer']
      # else:
      #    auth = None
      context = {
         "Trands":trands,
         # "auth":auth
      }
      return render(request,"home.html",context)


def login(request): 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       
        try:
            customer = Customer.objects.get(username=username)
            if customer.password==password:
               auth = {
                  'id':customer.id,
                  'username':customer.username,
                  'password':customer.password,
                  'email':customer.email,
                  'phone':customer.phone,
                  'profile':customer.profile,
                  'status':customer.status
               }
               request.session['customer'] = auth
               messages.success(request, f'Welcome, {customer.username}!')
               return redirect('/')  # Adjust redirect as needed
            else:
               messages.error(request, 'Incorrect password.')
        except Customer.DoesNotExist:
            messages.error(request, 'Customer with this email does not exist.')

    form = UserLoginForm()
    return render(request, 'auth/login.html', {'form':form, 'title':'log in'})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
       
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (Customer.objects.filter(username=username).exists() or Customer.objects.filter(email=email).exists()):
               Customer.objects.create(
                  username=username,                  
                  email=email,                 
                  password=password,           
                  status=1        
               )
               return redirect('login')    
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
                
    else:
        form = UserRegistrationForm()
        
    return render(request, 'auth/register.html', {'form' : form})

def logout(request):
   request.session.flush()  
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@xhr_request_only()
def menuList(request, *args, **kwargs):
   menus =  Menu.objects.filter(status="1").all()
   MenuHtml = ''
   for m in menus:
      if m.menuId == "":
         MenuHtml += (f'<li><button class="nav-link dropdown-btn" data-dropdown="dropdown{m.id}" aria-haspopup="true" aria-expanded="false" aria-label="discover">{m.name}<i class="bx bx-chevron-down" aria-hidden="true"></i></button>'
                        f'{menuLoop(menus,m.id)}'
                        f'</li>')  
   if 'customer' in request.session: 
      MenuHtml += f'<li ><a href="{settings.BASE_URL}logout" class="nav-link">Logout</a></li>'         
   else:                
      MenuHtml += f'<li ><a href="{settings.BASE_URL}login" class="nav-link">Login</a></li><li><a href="{settings.BASE_URL}register"  class="nav-link">Register</a></li>'      
   return JsonResponse({
            "Success": True,
            "Menus":MenuHtml
         }, status=200)


def menuLoop(Menus=[],MenuId=None,IsLoop=None):
   check = False
   if IsLoop:
      menu = f'<div id="dropdown{MenuId}" class="dropdown loopMenu"><ul role="menu">'
      arrow = '<i class="bx bx-chevron-down" aria-hidden="true"></i>'
   else:
      menu = f'<div id="dropdown{MenuId}" class="dropdown"><ul role="menu">'
      arrow = ''
   for m in Menus:
      if m.menuId:
         if m.menuId==str(MenuId):
            check = True
            menu += (f'<li><a class="dropdown-link dropdown-btn" data-dropdown="dropdown{m.id}" href="#" aria-haspopup="true" aria-expanded="false">{m.name}{arrow}</a>{menuLoop(Menus,m.id,True)}</li>')
   menu +='</ul></div>'
   if check:
      return menu
   else:    
      return ''

def postDetailView(request,Link=None):
      linkList = Link.split("+")
      MovieName = " ".join(linkList)
      data = Posts.objects.filter(name=MovieName,status=1).values().first()
      context = {
         "link":Link,
         "post":data,
      }
      return render(request,"detail.html",context)


@xhr_request_only()
def commentList(request, *args, **kwargs):
   post = kwargs.get('post', '')
   parent = request.GET.get('parent', None)
   startIndex = int(request.GET.get('index', 0))
   endIndex = int(request.GET.get('length', 3)) + startIndex
   if parent=='':
      parent = None
   lists =  Comment.objects.filter(post_id=post,parent_id=parent)[startIndex:endIndex].all()
   comments = []
   for i in lists:
      context = {
         'id':i.id,
         'msg':i.msg,
         'user':i.user.username,
         'more':Comment.objects.filter(parent_id=i.id).count(),
         'user_id':i.user.id,
         'parent':i.parent_id,
         'date':i.created_at
      }
      comments.append(context)
   return JsonResponse({
      "Success": True,
      "Comments":comments
   }, status=200)


@xhr_request_only()
def commentAdd(request, *args, **kwargs):
   if request.method == 'POST':
      post = kwargs.get('post', '')
      auth = False
      if 'customer' in request.session:
         auth = True
         msg = request.POST
         customer = request.session['customer']
         Comment.objects.create(
            msg=msg['message'],
            status=1,
            parent_id=msg['parent'],
            post_id=post,
            user_id=customer['id']
         )
      
      return JsonResponse({
         "Success": True,
         "Auth":auth,
         
      }, status=200)


# if customer.check_password(password):
#     login(request, customer)  # Logs the customer in without authenticate
#     messages.success(request, f'Welcome, {customer.username}!')
#     return redirect('/')  # Adjust redirect as needed
# else:
#     messages.error(request, 'Incorrect password.')