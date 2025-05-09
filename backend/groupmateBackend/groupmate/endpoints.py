import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from groupmate.model_classes.Course import Course
from groupmate.model_classes.EnrolledStudent import EnrolledStudent
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from groupmate.model_classes.Details import Student_Details


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_class_members(request):
    course_key = request.data.get("course_key")
    course = Course.objects.get(course_key=course_key)
    class_members = EnrolledStudent.objects.filter(course=course)
    students = []
    for member in class_members:
        student = {
            'username': member.student.user.username,
            'name': member.student.user.first_name + " " + member.student.user.last_name
        }
        students.append(student)
    return Response(students, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_class_feed(request):
    course_key = request.data.get("course_key")
    course = Course.objects.get(course_key=course_key)
    class_members = EnrolledStudent.objects.filter(course=course)

    students = []

    for member in class_members:
        try:
            details = Student_Details.objects.get(student=member.student, course=course)
            print(details.courses_taken)
            student = {
                'username': member.student.user.username,
                'name': member.student.user.first_name + " " + member.student.user.last_name,
                'project_proposal': details.vision,
                'skills': [skill['skill'] for skill in json.loads(details.skills)],
                'courses_taken': [f"{course['course_key']} {course['course_name']}" for course in json.loads(details.courses_taken)]
            }
            students.append(student)
        except Student_Details.DoesNotExist:
            pass
    return Response(students, status=status.HTTP_200_OK)