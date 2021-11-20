from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver


class Post(models.Model):
    body = models.TextField()
    picture = models.ImageField(upload_to='uploads/post', default='uploads/post/default.png', blank=True)
    created_on = models.DateTimeField(default=timezone.localtime())
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.localtime)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png',
                                blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Notification(models.Model):
    # 1 = Like, 2 = Comment, 3 = Follow
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)


