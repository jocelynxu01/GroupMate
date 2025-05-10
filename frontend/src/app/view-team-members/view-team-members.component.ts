import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../authorization.service';
import {MatCardModule} from '@angular/material/card';
import {MatChipsModule} from '@angular/material/chips';
import {MatExpansionModule} from '@angular/material/expansion';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-view-team-members',
  imports: [CommonModule,MatIconModule,FormsModule,MatCardModule,MatChipsModule,MatExpansionModule],
  templateUrl: './view-team-members.component.html',
  styleUrl: './view-team-members.component.css'
})
export class ViewTeamMembersComponent {
  constructor(private http: HttpClient, private router: Router, private auth: AuthService){}
  

  ngOnInit(): void {
    this.get_team_members(); 
    console.log('Course Key in OnInit:', this.auth.getStorage()?.getItem('course_key'));
  }
  team_members: Array<String> = []
  team_number = ''
  needed_skills: Array<String> = []
  current_skills: Array<String>=[]
  project_ideas: Array<String> = []
  message='Team allocation status'
  get_team_members(){
    const course_key = this.auth.getCourseKey()
    const token = this.auth.getAccessToken()
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
            this.needed_skills = response.body.needed_skills
            this.current_skills = response.body.current_skills
            this.project_ideas = response.body.project_ideas
            this.message=''
          }
          else{
            this.message = response.body.message;
          }
          
        },
        error: (error) => {
          console.error('Team details could not be retreived', error);
          this.message = "Team not allotted yet"
        }
      });
    
  }
  }

