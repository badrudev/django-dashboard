from django.db import models

# Create your models here.
from django.db import models


class Posts(models.Model):
    name = models.TextField()
    image = models.TextField()
    rate = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    lang = models.TextField()
    genre = models.TextField()
    story = models.TextField()
    link = models.CharField(max_length=100)
    more = models.TextField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Trand(models.Model):
    post = models.ForeignKey(Posts,related_name="posts", on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Menu(models.Model):
    name = models.CharField(max_length=100)
    menuId = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=100)
    

class Customer(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=128)  # Store hashed passwords
    profile = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Comment(models.Model):
    user = models.ForeignKey(Customer, related_name="user_comment", on_delete=models.CASCADE)
    msg = models.TextField()
    parent = models.ForeignKey(
        'self', related_name="replies", on_delete=models.CASCADE, null=True, blank=True
    )  # Allows threaded comments
    post = models.ForeignKey(Posts,related_name="post_comment",null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.msg[:20]}"
