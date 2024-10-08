from django.contrib import admin
from .models import Module,GroupPermission,UserAllow,ModuleAction

# Register your models here.
admin.site.register(Module)
admin.site.register(GroupPermission)
admin.site.register(UserAllow)
admin.site.register(ModuleAction)