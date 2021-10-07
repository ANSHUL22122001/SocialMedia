from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class user_details(models.Modelc


class detail(models.Model):
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    description = models.TextField()
    skill = models.CharField(max_length=40)
    pic_url = models.ImageField(upload_to='user_pics', default='user_pics/avatar.jpg')
    dark = models.BooleanField(default=False)
    follower = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)
    post = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.email}'


class otp_verify(models.Model):
    email = models.EmailField(max_length=30)
    otp = models.CharField(max_length=40)
    time_now = models.CharField(max_length=40)
    time_after = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.email}'


# class user_signed_up(models.Model):
#     email = models.EmailField(max_length=30)
#     password = models.CharField(max_length=100)
#     blocked = models.BooleanField(default=False)
# 
#     def __str__(self):
#         return f'{self.email}'
