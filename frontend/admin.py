from django.contrib import admin

# Register your models here.
from .models import Comment,Customer

# Register your models here.
admin.site.register(Comment)
admin.site.register(Customer)

