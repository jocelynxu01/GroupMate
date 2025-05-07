from django.urls import path
from .endpoints import create_class, get_classes,add_team_members


urlpatterns = [
    path('course/add/',create_class, name="create_course"),
    path('courses/',get_classes, name="instructor_get_classes"),
    path('teams/add',add_team_members, name="instructor_add_teams")
]