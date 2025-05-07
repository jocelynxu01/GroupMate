from django.contrib import admin
from .models import Profile
from .model_classes.Course import Course
# Register your models here.
admin.site.register(Profile)
admin.site.register(Course)