from django.urls import path
from .endpoints import create_class, get_classes,run_team_generator


urlpatterns = [
    path('course/add/',create_class, name="create_course"),
    path('courses/',get_classes, name="instructor_get_classes"),
    path('run-team-generator/',run_team_generator, name='run_team_generator')
]