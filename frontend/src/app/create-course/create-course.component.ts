import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {MatIconModule} from '@angular/material/icon';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-create-course',
  imports: [CommonModule, FormsModule, MatIconModule,MatFormFieldModule,MatInputModule, MatButtonModule],
  templateUrl: './create-course.component.html',
  styleUrl: './create-course.component.css'
})
export class CreateCourseComponent {
  course_name = ''

  constructor(private http: HttpClient, private router: Router){}

  create_course(){
    const token = localStorage.getItem("access_token");
    if(!token){
      this.router.navigate(['/login']);
      return;
    }
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const body = {
      "course_name":this.course_name
    }
    this.http.post<any>('http://127.0.0.1:8000/api/instructor/course/add/', body,{headers,observe: 'response' })
      .subscribe({
        next: (response) => {
          if(response.ok){
            const course_key = response.body.key;
            alert(`Course was added ${course_key}`);
            this.course_name = '';
          }
          
        },
        error: (error) => {
          console.error('Course could not added', error);
          
        }
      });
      this.router.navigate(['']);
  }
  }

