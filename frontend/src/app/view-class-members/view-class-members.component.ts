import { Component } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { AuthService } from '../authorization.service';
import { CommonModule } from '@angular/common';
import {MatTableModule} from '@angular/material/table';

@Component({
  selector: 'app-view-class-members',
  imports: [CommonModule,MatTableModule],
  templateUrl: './view-class-members.component.html',
  styleUrl: './view-class-members.component.css'
})
export class ViewClassMembersComponent {
  displayedColumns: string[] = ['username', 'name'];
  members: { name: string; username: string }[] = [];
  constructor(private http: HttpClient, private auth: AuthService){}
  ngOnInit(){
    this.get_class_members();
  }
  get_class_members(){
    let token = this.auth.getAccessToken();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const body = {
      "course_key":this.auth.getCourseKey()
    }
    
    this.http.post<any>('http://127.0.0.1:8000/api/view-class-members/',  body,{headers,observe: 'response' })
      .subscribe({
        next: (response) => {
          if(response.ok){
            let members_reponse = response.body;
            console.log(members_reponse)
            for (const member of members_reponse) {
              this.members.push({ 'name': member.name, 'username': member.username });
            }
            console.log('class members are: ',this.members)
          }
          
        },
        error: (error) => {
          console.error('Class members could not be retreived', error);
          
        }
      });
    }

  }

