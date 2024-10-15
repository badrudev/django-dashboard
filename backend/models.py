from django.db import models
from django.contrib.auth.models import User,Group

# Create your models here.
class Module(models.Model):
    module = models.CharField(max_length=255)
    moduleType = models.CharField(max_length=255,default=1)
    url = models.CharField(max_length=255,blank=True)
    status = models.CharField(max_length=255,default=1)
    parent_id = models.CharField(max_length=255,blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.module


class GroupPermission(models.Model):
    group = models.ForeignKey(Group,related_name="groups", on_delete=models.CASCADE)
    module = models.ForeignKey(Module,related_name="grouppermissions",on_delete=models.CASCADE)
    module_parent_id = models.CharField(max_length=255,blank=True)
    permission = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.permission


class UserAllow(models.Model):
    allow = models.TextField(blank=True, null=True)
    group = models.ForeignKey(Group, related_name="usergroup", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ModuleAction(models.Model):
    module = models.ForeignKey(Module,related_name="moduleaction",on_delete=models.CASCADE)
    module_parent_id = models.CharField(max_length=255,blank=True)
    permission = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.permission


# class GroupAllow(models.Model):
#     group = models.ForeignKey(Group, related_name="groupcreated", on_delete=models.CASCADE)
#     user  = models.ForeignKey(User, related_name="groupuser", on_delete=models.CASCADE)
#     created = models.DateField(auto_now_add=True)
#     updated = models.DateField(auto_now=True)

#     class Meta:
#         ordering = ['-created']

#     def __str__(self):
#         return self.group