import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from groupmate.model_classes.Course import Course
from groupmate.model_classes.EnrolledStudent import EnrolledStudent
from ..permissions import IsStudent
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from groupmate.model_classes.Details import Student_Details
from groupmate.model_classes.Team import Team
from ..models import Profile


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStudent])
def join_class(request):
    course_key = request.data.get("course_key")
    try:
        
        course = Course.objects.get(course_key = course_key)
        student = Profile.objects.get(user=request.user)
        enrollment, created = EnrolledStudent.objects.get_or_create(student=student,course=course)
        enrollment.save()

       
        return Response({'message':f'You successfully joined {course.course_name}'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message':f'Could not join {course_key}, exception: {e}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudent])
def get_classes(request):
    student = Profile.objects.get(user=request.user)
    enrollments = EnrolledStudent.objects.filter(student = student)
    
    enrolled_courses = []

    for e in enrollments:
        enrolled_courses.append(e.course.course_name)

    return Response({'enrolled_courses':enrolled_courses})

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStudent])
def fill_details(request):
    try:
        vision = request.data.get("vision")
        course_key = request.data.get("course_key")
        courses = request.data.get("courses_taken")
        student = Profile.objects.get(user=request.user)
        enrollment, _ = Student_Details.objects.get_or_create(
            student=student,
            courses_taken=json.dumps(courses),
            defaults={'vision': vision}
        )
        
        if not _:
            enrollment.vision = vision
            enrollment.save()
        enrollment.save()
        return Response({'message':f'Successfully filled details'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message':f'Error while filling details: {e}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStudent])
def get_team_details(request):
    course_key = request.data.get("course_key")
    course = Course.objects.get(course_key=course_key)
    student_profile = Profile.objects.get(user=request.user)
    student = EnrolledStudent.objects.get(student=student_profile,course=course)
    team_members = []
    if student.team_number:
        team  = Team.objects.get(team_number=student.team_number.team_number)
        students_in_team = EnrolledStudent.objects.filter(team_number=team)
        team_members = []
        for stu in students_in_team:
            tm = Profile.objects.get(user__username=stu.student.user.username)
            team_members.append(tm.user.username)

    return Response({"team_members": team_members,"team":student.team_number.team_number})
    