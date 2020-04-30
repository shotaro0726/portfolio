from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    prefectures = models.CharField(max_length=50, blank=True)
    works = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Idea_list(models.Model):
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.genre

class Opinion(models.Model):
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=100)
    idea_list = models.ForeignKey(Idea_list, on_delete=models.CASCADE)
    good = models.IntegerField(default=0)
    goodcheck = models.CharField(max_length=1000)

    def __str__(self):
        return self.idea_list.genre
