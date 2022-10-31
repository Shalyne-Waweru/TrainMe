from enum import unique
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, F

from cloudinary.models import CloudinaryField

from accounts.models import Owner, Trainer, User
from accounts.choices import *

# Create your models here.
class Dog(models.Model):
    user = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='dog')
    dog_name = models.CharField(max_length=50)
    dog_age = models.IntegerField()
    dog_pic = CloudinaryField('image')
    dog_sex = models.CharField(max_length=10,choices=gender)
    
    def __str__(self):
        return self.dog_name
    
class Clinic(models.Model):
    clinic_name = models.CharField(max_length=50)
    clinic_location=models.CharField(max_length=50, choices=places)
    user=models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='clinic')
    
    def __str__(self):
        return self.clinic_owner + ' ' + self.clinic_name
    
    @classmethod   
    def filter_by_user(cls, user):
        clinics = cls.objects.filter(user__id__icontains=user).all()
        return clinics
        
class BusinessHours(models.Model):
    day= models.CharField(max_length=10, choices=DAYS_OF_WEEK, unique=True)
    start = models.TimeField(blank=True)
    end = models.TimeField(blank=True)
    open_closed= models.BooleanField(default=False)
    user= models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='business_hours')
    
    def __str__(self):
        return self.user.user.username + ' ' + self.day
    
    @classmethod   
    def filter_by_user(cls, user):
        hours = cls.objects.filter(user__id__icontains=user).all()
        return hours
    
    def clean(self):
        if self.start > self.end:
            raise ValidationError('Start should be before end')
        return super().clean()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(
                    start__lte=F('end')
                ),
                name='start_before_end'
            )
        ]
    
    
    
class Review(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer')
    reviewed =models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='reviewed')
    
    def __str__(self):
        return self.reviewer.username + ' ' + self.title
    
    @classmethod
    def get_trainer_reviews(cls, id):
        reviews = Review.objects.filter(reviewed__pk=id)
        return reviews
    
class Post(models.Model):
    video_title = models.CharField(max_length=100)
    video_caption = models.TextField()
    video = CloudinaryField(resource_type='video', blank=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        return self.user.username + ' ' + self.video_title
    
    @classmethod   
    def filter_by_user(cls, user):
        posts = cls.objects.filter(user__id__icontains=user).all()
        return posts
    
class Booking(models.Model):
    email= models.EmailField()
    user= models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='bookings')
    trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='book')
    date= models.DateField()
    time= models.TimeField(unique=True)
    
    def __str__(self):
        return self.user.user.username + ' ' + self.trainer.user.username