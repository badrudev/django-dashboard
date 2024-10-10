from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm
 
urlpatterns = [
        # path('index', views.index, name ='index'),
        path('register/', views.register, name='register'),
        path('login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=UserLoginForm), name='login'),
        # path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
        path('logout/', views.logout,name='logout'),

        # Dashboard Url
        path('dashboard/', views.dashboard, name ='dashboard'),
        path('administration/permission',views.permission),
        path('administration/permission/<int:roleId>/',views.rolePermission,name="role-permission"),
        path('administration/permission/<int:roleId>/<int:parentId>',views.rolePermission),
        path('administration/permission/save/<int:roleId>',views.savePermission,name="save-permission"),
        
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
    
        # path('plugin/chart',views.graphChart),
        path('administration/module/',views.module,name="module"),
        path('administration/module/<int:parentId>',views.module,name="module"),
        # path('administration/module/<int:parentId>/',views.module,name="module"),
        path('administration/module/add/',views.addEditModule),
        path('administration/module/add/<int:parentId>',views.addEditModule),
        path('administration/module/<int:moduleId>/delete',views.deleteModule),
        # path('administration/module/<int:moduleId>/edit',views.addeditModule),
        # path('module/add/<int:parentId>',views.addModule,name="add-module"),
        # path('module/list',views.moduleList,name="module-list"),
        # path('module/edit/<int:moduleId>',views.moduleEdit),
        path('sidebar/list',views.sidebarList,name="sidebar-list"),
        path('redirect',views.redirect,name="redirect"),
        # path('notFound',views.notFound,name="notFound"),
 

]