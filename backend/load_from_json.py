import requests
import logging
import json
logger = logging.getLogger(__name__)

def create_profile(username, first_name, last_name, email):
    body = {
        "username":username,
        "first_name":first_name,
        "last_name":last_name,
        "email":email,
        "password":f"hello*{username}",
        "role":"Student"
    }
    
    url = "http://127.0.0.1:8000/api/register/"
    print(body)
    response = requests.post(url, json=body)
    if(response.status_code==requests.codes.ok):
        logger.info(f"{username} was registerd with password hello*{username}")
    else:
        logger.error(f"{username} was not registered {response.text}")
def login(cred, course_key):
    url = "http://127.0.0.1:8000/login/"
    print(cred)
    response = requests.post(url, json=cred)
    if(response.status_code==requests.codes.ok):
        access_token = json.loads(response.text)['access']
        logger.info(f"{cred['username']} logged in")
        # join_class(course_key,access_token,cred['username'])
        return access_token
        #join course
    else:
        logger.error(f"{cred['username']} not logged in {response.text}")
    return ''
def join_class(course_key, username, access_token):
    url = "http://127.0.0.1:8000/api/student/course/join/"
    headers= {"Authorization":f"Bearer {access_token}"}
    body = {"course_key": course_key}
    response = requests.post(url, headers=headers,json=body)
    logger.info(f"User {username}'s status of joining course {response.text}")
def fill_details(username, vision, skills, courses_taken, course_key, access_token):
    url="http://127.0.0.1:8000/api/student/courses/fillDetails"
    body={
        "course_key":course_key,
        "courses_taken": [{'course_key':'', 'course_name':course} for course in courses_taken],
        "vision":vision,
        "skills":[{'skill':skill} for skill in skills]
    }
    headers= {"Authorization":f"Bearer {access_token}"}
    response = requests.post(url, json=body,headers=headers)
    logger.info(f"{username} status of adding details: {response.text}")
  
def main():
    lines = []
    with open("vision_students.json","r") as file:
        lines = file.read()
        
    lines = json.loads(lines)
    
    course_key = "2f0c5439-7185-4998-977e-723815bdb321"
    for line in lines:
        username = line['id']
        cred = {
            'username':username,
            'password':f'hello*{username}'
        }
        # create_profile(line['id'],line['first_name'],line['last_name'],line['email'])
        token = login(cred,course_key)
        if (token!=''):
            join_class(course_key,username, token)
            fill_details(line['id'],line['vision'],line['skills'],line['courses'],course_key,token)
            
    
    
    
if __name__=="__main__":
    logging.basicConfig(filename='load_from_json.log', level=logging.INFO)
    main()