from django.contrib import admin

from .models import Booking, Hours, Clinic, Dog, Post, Review, Service

# Register your models here.
admin.site.register(Dog)
admin.site.register(Review)
admin.site.register(Post)
admin.site.register(Clinic)
admin.site.register(Hours)
admin.site.register(Booking)
admin.site.register(Service)