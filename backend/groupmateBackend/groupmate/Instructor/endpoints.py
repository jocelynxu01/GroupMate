from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from groupmate.model_classes.Course import Course
from groupmate.model_classes.Team import Team
from groupmate.model_classes.EnrolledStudent import EnrolledStudent
from ..permissions import IsInstructor
from rest_framework.permissions import IsAuthenticated
from ..serializers import CourseSerializer
from ..models import Profile
import uuid
from rest_framework import status



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsInstructor])
def create_class(request):
    course_name = request.data.get("course_name")
    key = uuid.uuid4()
    instructor = Profile.objects.get(user=request.user)
    course = Course.objects.create(course_name=course_name, course_key = key, created_by =instructor)
    course.save()
    return Response({'key':key, 'course_name':course_name})

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsInstructor])
def get_classes(request):
    instructor = Profile.objects.get(user=request.user)
    courses = Course.objects.filter(created_by = instructor)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsInstructor])
def add_team_members(request):
    try:
        course_key = request.data.get("course_key")
        course = Course.objects.get(course_key=course_key)
        team = Team.objects.create(course = course)
  
        team_members = request.data.get("team_members")
        
        for i in team_members:
            try:
                student = Profile.objects.get(user__username=i)
                enrolled = EnrolledStudent.objects.get(student=student, course=course)
                enrolled.team_number = team
                enrolled.save()
            except Exception as e:
                return Response(
                    {'error': f"Student '{i}' is not enrolled in course '{course.course_name}'."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response({"message":f"Team members are added to team {team.team_number}"})
    except Exception as e:
        return Response(f"Error happened while adding members to team: {e}",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
