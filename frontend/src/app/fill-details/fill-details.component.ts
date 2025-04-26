import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-fill-details',
  imports: [CommonModule, FormsModule],
  templateUrl: './fill-details.component.html',
  styleUrl: './fill-details.component.css'
})
export class FillDetailsComponent {
  courses: { course_code: string; course_name: string }[] = [];
  vision_essay = ''
  constructor(private http: HttpClient, private router: Router){};
  add_course(){
    this.courses.push({course_code:'', course_name:''});
  }
  fill_details(){
    const body = {
      "vision": this.vision_essay,
      "courses_taken":this.courses
    }
    const token = localStorage.getItem("access_token");
    if(!token){
      this.router.navigate(['/login']);
      return;
    }
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    this.http.post<any>('http://127.0.0.1:8000/api/student/courses/fillDetails', body,{headers,observe: 'response' })
      .subscribe({
        next: (response) => {
          if(response.ok){
            
            alert(`You have successfully provided the details`);
            this.router.navigate(['/home'])
          }
          
        },
        error: (error) => {
          console.error('Could not add details', error);
          
        }
      });
  }
}
