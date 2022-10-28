from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

# Create your models here.
class User(AbstractUser):
    is_trainer = models.BooleanField('Dog_Trainer', default=False)
    is_owner = models.BooleanField('Dog_Owner', default=False)
    phone= models.CharField(max_length=10)
    
places=(
    ('Nairobi-CBD', 'Nairobi-CBD'),
    ('Nairobi-Ngong Road', 'Nairobi-Ngong Road'),
    ('Nairobi-Thika Road', 'Nairobi-Thika Road'),
    ('Nairobi-Waiyaki Way', 'Nairobi-Waiyaki Way'),
    ('Nairobi-Outering Road', 'Nairobi-Outering Road'),
    ('Nairobi-Jogoo Road', 'Nairobi-Jogoo Road'),
    ('Nairobi-Kiambu Road', 'Nairobi-Kiambu Road'),
    ('Nairobi-Westlands', 'Nairobi-Westlands'),
    ('Kiambu', 'Kiambu'),
    ('Kisii', 'Kisii'),
    ('Kikuyu', 'Kikuyu'),
    ('Nakuru', 'Nakuru'),
    ('Eldoret', 'Eldoret'),
    ('Kakamega', 'Kakamega'),
    ('Kisumu', 'Kisumu'),
    ('Mombasa', 'Mombasa'),      
)
gender=(
    ('male', 'male'),
    ('female', 'female'),
)
services=(
    ('Obedience Training', 'Obedience Training'),
    ('Trick Skill Training', 'Trick Skill Training'),
    ('Behavior Modification', 'Behavior Modification'),
    ('Puppy Training', 'Puppy Training'),
    ('Security Program', 'Security Program'),
    ('Separation Anxiety', 'Separation Anxiety')
)

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Dog_Trainer")
    image = CloudinaryField('image')
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