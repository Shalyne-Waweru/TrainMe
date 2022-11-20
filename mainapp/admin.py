from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Dog)
admin.site.register(Review)
admin.site.register(Post)
admin.site.register(Clinic)
admin.site.register(Hours)
admin.site.register(Booking)