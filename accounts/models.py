from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from .choices import *

# Create your models here.
class User(AbstractUser):
    is_trainer = models.BooleanField('Dog_Trainer', default=False)
    is_owner = models.BooleanField('Dog_Owner', default=False)
    phone= models.CharField(max_length=10)

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Dog_Trainer")
    image = CloudinaryField('image')
    bio = models.TextField()
    gender = models.CharField(max_length=10, choices= gender)
    services =models.CharField(max_length=255, choices=services)
    location= models.CharField(max_length=40, choices = places)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user(sender, instance, created, dispatch_uid="Dog_Trainer", **kwargs):
        if instance.is_trainer:
            if created:
                Trainer.objects.get_or_create(user = instance)

    def save_profile(self):
        self.save()


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Dog_Owner")
    location= models.CharField(max_length=40, choices = places)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user(sender, instance, created, dispatch_uid="Dog_Owner", **kwargs):
        if instance.is_owner:
            if created:
                Owner.objects.get_or_create(user = instance)

    def save_profile(self):
        self.save()