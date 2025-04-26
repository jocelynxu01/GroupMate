import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../authorization.service';
@Component({
  selector: 'app-list-classes-student',
  imports: [CommonModule, FormsModule],
  templateUrl: './list-classes-student.component.html',
  styleUrl: './list-classes-student.component.css'
})
export class ListClassesStudentComponent {
  constructor(private http: HttpClient, private router: Router, private auth: AuthService){}
  courses : Array<String>= [];
  ngOnInit(): void {
    this.get_courses(); 
  }
  get_courses(){
    
    const token = this.auth.getAccessToken();
    if(!token){
      this.router.navigate(['/login']);
      return;
    }
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.get<any>('http://127.0.0.1:8000/api/student/courses/', {headers,observe: 'response' })
      .subscribe({
        next: (response) => {
          if(response.ok){
            let response_courses = response.body.enrolled_courses;
            for (const course of response_courses) {
              this.courses.push(course);
            }
          }
          
        },
        error: (error) => {
          console.error('Courses could not be retreived', error);
          
        }
      });
    
  }
  }

