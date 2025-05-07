from django.db import models
from .Course import Course
from .Team import Team
from ..models import Profile

class EnrolledStudent(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True)
    team_number = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)