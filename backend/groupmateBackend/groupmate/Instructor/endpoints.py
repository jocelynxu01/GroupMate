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

def assign_teams_helper(course_key, team_members,needed_skills, current_skills, project_ideas):
    
    course = Course.objects.get(course_key=course_key)
    team = Team.objects.create(course = course, needed_skills=needed_skills, current_skills=current_skills, project_ideas=project_ideas)

    for i in team_members:
        student = Profile.objects.get(user__username=i)
        enrolled = EnrolledStudent.objects.get(student=student, course=course)
        enrolled.team_number = team
        enrolled.save()
        

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
    # print(json.dumps(students))
    try:
        groups = run_model(students)
    except Exception as e:
        return Response({'message':f'Creating teams failed {e}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    for group in groups:
        member_ids = [m["username"] for m in group["members"]]
        try:
            assign_teams_helper(course_key=course_key,team_members=member_ids,needed_skills=group["needed_skills"],current_skills=group["current_skills"],project_ideas=group["project_ideas"])
        except Exception as e:
            return Response({'message':f'Creating teams failed {e}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #return a different message for failure based on what run_model returns
    print('response is',Response({'message':f'Successfully created {len(groups)} teams'},status=status.HTTP_200_OK))
        
    return Response({'message':'Successfully created teams'},status=status.HTTP_200_OK)

