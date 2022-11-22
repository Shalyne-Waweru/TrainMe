from django.db import models
from django.db.models import signals
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from .choices import *
from django.contrib.postgres.fields import ArrayField

# from django.contrib.auth.signals import user_logged_in
# from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    is_trainer = models.BooleanField('Dog_Trainer', default=False)
    is_owner = models.BooleanField('Dog_Owner', default=False)
    phone= models.CharField(max_length=12)
class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Dog_Trainer")
    image = CloudinaryField('image')
    bio = models.TextField()
    gender = models.CharField(max_length=10, choices= gender)
    services=ArrayField(models.CharField(max_length=100, choices=service), null=True, blank=True)
    location= models.CharField(max_length=40, choices = places)
    price_charge= models.IntegerField(default=1000)
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
    
    @classmethod  
    def search_by_location(cls, search_term):
        loc = cls.objects.filter(location__icontains=search_term)
        return loc
    
    @classmethod
    def filter_by_service(cls, service):
        images = cls.objects.filter(services__icontains=service).all()
        return images
    
    @classmethod
    def filter_by_gender(cls, gender):
        sex = cls.objects.filter(gender__icontains=gender).all()
        return sex


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Dog_Owner")
    location= models.CharField(max_length=40, choices = places)
    image = CloudinaryField('image')
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
        
        
class UserLogin(models.Model):
    """Represent users' logins, one per record"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login') 
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return self.user.username



    # def update_user_login(sender, user, **kwargs):
    #     user.userlogin_set.create(timestamp=timezone.now())
    #     user.save()

    # user_logged_in.connect(update_user_login)
    
    def user_presave(sender, instance, **kwargs):
        if instance.last_login:
            old = instance.__class__.objects.get(pk=instance.pk)
            if instance.last_login != old.last_login:
                instance.login.create(timestamp=instance.last_login)

    signals.pre_save.connect(user_presave, sender=User)