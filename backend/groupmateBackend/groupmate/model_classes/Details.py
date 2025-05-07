from django.db import models
from ..models import Profile
from .Course import Course

class Student_Details(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    courses_taken = models.TextField(blank=True, default='[]')
    #details - other
    vision = models.TextField(max_length=1000,blank=True)