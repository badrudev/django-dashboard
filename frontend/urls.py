from django.urls import path
#now import the views.py file into this code
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
  path('',views.home,name="home"),
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  # path('movie/posts',views.posts),
  # path('movie/trand',views.trand),
  path('menuList',views.menuList),
  path('commentList/<str:post>',views.commentList),
  path('commentAdd/<str:post>',views.commentAdd),
  # path('movie/menu',views.menu),
  # path('movie/menu/<int:pId>',views.menu),
  # path('movie/posts/<int:id>',views.posts),
  # path('movie/posts/<int:id>/add-edit',views.postAddEditView),
  # path('movie/posts/add-edit',views.postAddEditView),
  path('detail/<str:Link>',views.postDetailView),
 
 
]
