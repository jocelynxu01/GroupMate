from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from groupmate.model_classes.Course import Course
from groupmate.model_classes.Team import Team
from groupmate.model_classes.EnrolledStudent import EnrolledStudent
from groupmate.model_classes.Details import Student_Details
from ..permissions import IsInstructor
from rest_framework.permissions import IsAuthenticated
from ..serializers import CourseSerializer
from ..models import Profile
import uuid
from rest_framework import status
import json
from ..Team_Generator.team_generator import run_model

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

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsInstructor])
def run_team_generator(request):
    course_key = request.data.get("course_key")
    course = Course.objects.get(course_key=course_key)
    class_members = EnrolledStudent.objects.filter(course=course)

    students = []

    for member in class_members:
        
        details = Student_Details.objects.get(student=member.student)
        student = {
            'username': member.student.user.username,
            'name': member.student.user.first_name + " " + member.student.user.last_name,
            'project_proposal': details.vision,
            'skills': [skill['skill'] for skill in json.loads(details.skills)],
            'courses_taken':json.loads(details.courses_taken),
        }
        students.append(student)

        run_model(json.dumps(students))
        #return a different message for failure based on what run_model returns
        return Response({'message':'Successfully created teams'},status=status.HTTP_200_OK)

