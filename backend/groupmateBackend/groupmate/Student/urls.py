from django.urls import path
from .endpoints import join_class, get_classes, fill_details,get_team_details

urlpatterns = [
    path('course/join/',join_class, name="join_course"),
    path('courses/',get_classes, name="student_get_classes"),
    path('courses/fillDetails',fill_details, name="student_fill_details"),
    path('team/get',get_team_details, name="get_team_details")
]