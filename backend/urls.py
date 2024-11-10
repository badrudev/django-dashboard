from django.urls import path
from django.conf import settings
# from . import views
from .controllers import movie_controller, auth_controller, dashboard_controller,chat_controller
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm


urlpatterns = [
        # Auth Url
        path('register/', auth_controller.register, name='register'),
        path('login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=UserLoginForm), name='login'),
        # path('login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=UserLoginForm), name='login'),
        # path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
        # path('logout/', auth_controller.logout,name='logout'),
        path('logout/', auth_controller.logout, name='login'),
        
        
        # Dashboard Url
        path('dashboard/', dashboard_controller.dashboard, name ='dashboard'),

        # Administration permission
        path('administration/permission',dashboard_controller.permission),
        path('administration/permission/<int:roleId>/delete',dashboard_controller.deletePermission),
        path('administration/permission/add',dashboard_controller.addEditPermission),
        path('administration/permission/<int:roleId>/',dashboard_controller.rolePermission,name="role-permission"),
        path('administration/permission/<int:roleId>/<int:parentId>',dashboard_controller.rolePermission),
        path('administration/permission/save/<int:roleId>',dashboard_controller.savePermission,name="save-permission"),

        # Administration module
        path('administration/module/',dashboard_controller.module,name="module"),
        path('administration/module/<int:parentId>',dashboard_controller.module,name="module"),
        path('administration/module/add/',dashboard_controller.addEditModule),
        path('administration/module/add/<int:parentId>',dashboard_controller.addEditModule),
        path('administration/module/<int:moduleId>/delete',dashboard_controller.deleteModule),

        # Administration user
        path('administration/user',dashboard_controller.user,name="user"),
        path('administration/user/add/<int:userId>',dashboard_controller.addEditUser),
        path('administration/user/add/',dashboard_controller.addEditUser),


        # Movie Url
        path('movie/post',movie_controller.movieList,name="movie-list"),
        path('movie/post/add',movie_controller.movieAdd,name="movie-add"),
        path('movie/post/<int:postId>/edit',movie_controller.movieEdit),
        path('movie/post/<int:postId>/delete',movie_controller.movieDelete),
        path('movie/menu/',movie_controller.menuList),
        path('movie/menu/<int:parentId>',movie_controller.menuList),
        path('movie/menu/add/',movie_controller.menuAdd,name="menu-add"),
        path('movie/menu/add/<int:parentId>',movie_controller.menuAdd),
        path('movie/menu/edit/<int:menuId>',movie_controller.menuEdit),
        path('movie/menu/<int:menuId>/delete',movie_controller.menuDelete),

        # Sidebar 
        path('sidebar/list',dashboard_controller.sidebarList,name="sidebar-list"),

        # Chat view
        path('chat/list',chat_controller.ChatView.as_view(greeting="G'day"),name="sidebar-list"),



]
 
"""  
urlpatterns = [
        # path('index', views.index, name ='index'),
        path('register/', views.register, name='register'),
        path('login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=UserLoginForm), name='login'),
        # path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
        path('logout/', views.logout,name='logout'),

        # Dashboard Url
        path('dashboard/', views.dashboard, name ='dashboard'),

        # Administration permission
        path('administration/permission',views.permission),
        path('administration/permission/<int:roleId>/delete',views.deletePermission),
        path('administration/permission/add',views.addEditPermission),
        path('administration/permission/<int:roleId>/',views.rolePermission,name="role-permission"),
        path('administration/permission/<int:roleId>/<int:parentId>',views.rolePermission),
        path('administration/permission/save/<int:roleId>',views.savePermission,name="save-permission"),

        # Administration module
        path('administration/module/',views.module,name="module"),
        path('administration/module/<int:parentId>',views.module,name="module"),
        path('administration/module/add/',views.addEditModule),
        path('administration/module/add/<int:parentId>',views.addEditModule),
        path('administration/module/<int:moduleId>/delete',views.deleteModule),

        # Administration user
        path('administration/user',views.user,name="user"),
        path('administration/user/add/<int:userId>',views.addEditUser),
        path('administration/user/add/',views.addEditUser),

        
        # Movie Url
        path('movie/post',views.movieList,name="movie-list"),
        path('movie/post/add',views.movieAdd,name="movie-add"),
        path('movie/post/<int:postId>/edit',views.movieEdit),
        path('movie/post/<int:postId>/delete',views.movieDelete),

        path('movie/menu/',views.menuList),
        path('movie/menu/<int:parentId>',views.menuList),
        path('movie/menu/add/',views.menuAdd,name="menu-add"),
        path('movie/menu/add/<int:parentId>',views.menuAdd),
        path('movie/menu/edit/<int:menuId>',views.menuEdit),
        path('movie/menu/<int:menuId>/delete',views.menuDelete),


        # socket
        path('socket/chat',views.chat),
    
        
        path('sidebar/list',views.sidebarList,name="sidebar-list"),
        path('redirect',views.redirect,name="redirect"),
] 

"""


