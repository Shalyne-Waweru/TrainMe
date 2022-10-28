from django.contrib import admin

from .models import Dog, Post, Review

# Register your models here.
admin.site.register(Dog)
admin.site.register(Review)
admin.site.register(Post)