from django.db import models
from ..models import Profile
class Course(models.Model):
    course_name = models.TextField(max_length=100, blank=True)
    course_key = models.UUIDField()
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)