import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-list-classes-instructor',
  imports: [CommonModule, FormsModule],
  templateUrl: './list-classes-instructor.component.html',
  styleUrl: './list-classes-instructor.component.css'
})
export class ListClassesInstructorComponent {
  constructor(private http: HttpClient, private router: Router){}
  courses: { course_name: string; course_key: string }[] = [];
  ngOnInit(): void {
    this.get_courses(); 
  }
  get_courses(){
    
    const token = localStorage.getItem("access_token");
    if(!token){
      this.router.navigate(['/login']);
      return;
    }
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.get<any>('http://127.0.0.1:8000/api/instructor/courses/', {headers,observe: 'response' })
      .subscribe({
        next: (response) => {
          if(response.ok){
            let response_courses = response.body;
            for (const course of response_courses) {
              this.courses.push({ 'course_name': course.course_name, 'course_key': course.course_key });
            }
          }
          
        },
        error: (error) => {
          console.error('Courses could not be retreived', error);
          
        }
      });
    
  }
  }

