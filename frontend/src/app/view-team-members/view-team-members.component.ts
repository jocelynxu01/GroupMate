import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-view-team-members',
  imports: [CommonModule, FormsModule],
  templateUrl: './view-team-members.component.html',
  styleUrl: './view-team-members.component.css'
})
export class ViewTeamMembersComponent {
  constructor(private http: HttpClient, private router: Router){}
  

  ngOnInit(): void {
    this.get_team_members(); 
    console.log('Course Key in OnInit:', localStorage.getItem('course_key'));
  }
  team_members: Array<String> = []
  team_number = ''
  get_team_members(){
    const course_key = localStorage.getItem("course_key")
    const token = localStorage.getItem("access_token");
    console.log(course_key, token)
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const body = {
      'course_key': course_key
    }
    this.http.post<any>('http://127.0.0.1:8000/api/student/team/get', body,{headers,observe: 'response' })
      .subscribe({
        next: (response) => {
          if(response.ok){
            let members = response.body.team_members;
            for (const member of members) {
              this.team_members.push(member);
            }
            this.team_number = response.body.team
          }
          
        },
        error: (error) => {
          console.error('Courses could not be retreived', error);
          
        }
      });
    
  }
  }

