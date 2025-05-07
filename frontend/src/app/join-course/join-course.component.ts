import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-create-course',
  imports: [CommonModule, FormsModule],
  templateUrl: './join-course.component.html',
  styleUrl: './join-course.component.css'
})
export class JoinCourseComponent {
  course_key = ''

  constructor(private http: HttpClient, private router: Router){}

  join_course(){
    const token = localStorage.getItem("access_token");
    if(!token){
      this.router.navigate(['/login']);
      return;
    }
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const body = {
      "course_key":this.course_key
    }
    this.http.post<any>('http://127.0.0.1:8000/api/student/course/join/', body,{headers,observe: 'response' })
      .subscribe({
        next: (response) => {
          if(response.ok){
            
            alert(`You have joined the course`);
            localStorage.setItem("course_key",this.course_key);
            this.course_key = '';
          }
          
        },
        error: (error) => {
          console.error('Course could not be joined', error);
          
        }
      });
    
  }
  }

