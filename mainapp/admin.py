from django.contrib import admin

from .models import Booking, BusinessHours, Clinic, Dog, Post, Review

# Register your models here.
admin.site.register(Dog)
admin.site.register(Review)
admin.site.register(Post)
admin.site.register(Clinic)
admin.site.register(BusinessHours)
admin.site.register(Booking)