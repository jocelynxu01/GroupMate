from django.urls import path
from .views import RegisterView
from .views import profile_view, get_role
from django.urls import path,include
from .Instructor import urls as instructor_urls
from .Student import urls as student_urls
from .endpoints import get_class_members,get_class_feed

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('getrole/',get_role,name="get_role"),
    path('profile/<str:username>/', profile_view, name='profile_view'),
    #common
    path('view-class-members/',get_class_members, name='get_class_members'),
    path('view-class-feed/',get_class_feed,name='get_class_feed'),
    #instructors
    path('instructor/', include(instructor_urls)),

    #students
    path('student/',include(student_urls))
]
