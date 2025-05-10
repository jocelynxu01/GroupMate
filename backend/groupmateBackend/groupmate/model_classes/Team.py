from django.db import models
from .Course import Course


class Team(models.Model):
    team_number = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    #any other details like team ideas you want to store
    needed_skills = models.TextField(blank=True, default='[]')
    current_skills = models.TextField(blank=True, default='[]')
    project_ideas = models.TextField(blank=True)