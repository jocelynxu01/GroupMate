import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../authorization.service';
import { CommonModule } from '@angular/common';
import {MatCardModule} from '@angular/material/card';
import {MatChipsModule} from '@angular/material/chips';
@Component({
  selector: 'app-class-feed',
  imports: [CommonModule,MatCardModule, MatChipsModule],
  templateUrl: './class-feed.component.html',
  styleUrl: './class-feed.component.css'
})
export class ClassFeedComponent {
  constructor(private http: HttpClient, private auth: AuthService){}
  details:{"username":string,"name": string, project_proposal:string, skills: string[], courses_taken: string[]}[]=[]
  ngOnInit(){
    this.get_class_feed();
  }
  get_class_feed(){
    let course_key = this.auth.getCourseKey();
    let token = this.auth.getAccessToken();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const body = {
      "course_key":course_key
    }
    this.http.post<any>('http://127.0.0.1:8000/api/view-class-feed/', body,{headers,observe: 'response' })
      .subscribe({
        next: (response) => {
          if(response.ok){

            const details_reponse = response.body;
            for (const detail of details_reponse) {
                let skills: string[] = []
                for (const skill of detail.skills){
                  skills.push(skill);
                }
                console.log(skills)
                let courses: string[] = []
                for (const course of detail.courses_taken){
                  courses.push(course);
                }
                let temp = {
                  "username": String(detail.username),
                  "name": String(detail.name),
                  "project_proposal": String(detail.project_proposal),
                  "skills": skills,
                  "courses_taken": courses
                  

                }
                this.details.push(temp);
            }
          }
          console.log(this.details)
          
        },
        error: (error) => {
          console.error('Error while accessing class feed', error);
          
        }
      });
      
  }

  }

