from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, F

from cloudinary.models import CloudinaryField

from accounts.models import Owner, Trainer, User
from accounts.choices import *

# Create your models here.
class Dog(models.Model):
    user = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='dogs')
    dog_name = models.CharField(max_length=50)
    dog_breed= models.CharField(max_length=200, choices=breed)
    dog_age = models.IntegerField()
    dog_pic = CloudinaryField('image')
    dog_sex = models.CharField(max_length=10,choices=gender)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.user.username+'s' + ' ' + self.dog_name
    
    @classmethod   
    def filter_by_user(cls, user):
        dogs = cls.objects.filter(user__id__icontains=user).all()
        return dogs
    
class Clinic(models.Model):
    clinic_name = models.CharField(max_length=50, unique=True)
    clinic_location=models.CharField(max_length=50, choices=places)
    user=models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='clinic')
    
    def __str__(self):
        return self.clinic_name + ' ' + self.user.user.username+" 's Clinic"
    
    @classmethod   
    def filter_by_user(cls, user):
        clinics = cls.objects.filter(user__id__icontains=user).all()
        return clinics
        
class Hours(models.Model):
    user= models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='business_hours')
    day= models.CharField(max_length=10, choices=DAYS_OF_WEEK, unique=True)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    open_closed= models.BooleanField(default=False)
    
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
    date = models.DateTimeField(auto_now_add=True)
    
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
    user= models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='posts')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.user.username + ' ' + self.video_title
    
    @classmethod   
    def filter_by_user(cls, user):
        posts = cls.objects.filter(user__id__icontains=user).all()
        return posts
    
class Booking(models.Model):
    user= models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='bookings')
    trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='book')
    created_date = models.DateTimeField(auto_now_add=True)
    book_date = models.DateField(null=True)
    book_time = models.TimeField(null=True)
    booking_number = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.booking_number

    def save(self, **kwargs):
        if not self.booking_number:
            self.booking_number = f"{self.book_date:%Y%m%d}{self.book_time:%H%M}"
        super().save(**kwargs)
        
    @classmethod
    def filter_by_trainer(cls, id):
        books = cls.objects.filter(trainer__pk=id)
        return books
    
    @classmethod
    def filter_by_owner(cls, user):
        bookings = cls.objects.filter(user__id__icontains=user).all()
        return bookings