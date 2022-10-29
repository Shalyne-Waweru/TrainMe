from tkinter import CASCADE
from django.db import models

from cloudinary.models import CloudinaryField

from accounts.models import Owner, Trainer, User, gender

# Create your models here.
class Dog(models.Model):
    dog_owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='dog')
    dog_name = models.CharField(max_length=50)
    dog_age = models.IntegerField()
    dog_pic = CloudinaryField('image')
    dog_sex = models.CharField(max_length=10,choices=gender)
    
    def __str__(self):
        return self.dog_name
        
class Review(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer')
    reviewed =models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='reviewed')
    
    def __str__(self):
        return self.reviewer + ' ' + self.title
    
class Post(models.Model):
    video_title = models.CharField(max_length=100)
    video_caption = models.TextField()
    video = CloudinaryField(resource_type='video', blank=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        return self.user.username + ' ' + self.video_title