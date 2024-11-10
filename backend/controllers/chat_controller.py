from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.views import View

class ChatView(View):
    greeting = "Good Day"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        print(self.greeting)

    def dispatch(self, request, *args, **kwargs):
        # self.user = request.user
        if self.user.is_authenticated:
            return HttpResponseRedirect(settings.BASE_URL + 'admin/login')
            # return HttpResponseRedirect(reverse('admin_login'))
        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user


    def get(self, request):
        if self.user.is_authenticated:
            greeting = f"{self.greeting}, {self.user.username}!"
        else:
            greeting = "Hello, Guest!"
        
        return HttpResponse(f"{greeting} {self.greeting}")
 

