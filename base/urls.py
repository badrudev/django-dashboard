
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth
 

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('admin/', include('backend.urls')),
    
]
