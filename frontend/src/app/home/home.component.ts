import { Component } from '@angular/core';
import { AuthService } from '../authorization.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { HttpHeaders, HttpClient} from '@angular/common/http';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSelectModule} from '@angular/material/select';
import {MatListModule} from '@angular/material/list';
import {MatCardModule} from '@angular/material/card';
@Component({
  selector: 'app-home',
  imports: [CommonModule, 
    FormsModule, 
    RouterOutlet,
     MatButtonModule, 
     MatToolbarModule, 
     MatIconModule,
     MatSidenavModule, 
     MatFormFieldModule,
    MatSelectModule,
    MatListModule,
  MatCardModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  showFiller = true;
  course_icon = "content_copy"
  selectedCourse: string = '';
    instructor = false;
    student = false;
    courses: { course_name: string; course_key: string }[] = [];
    course_key: any = '';
    show_course_key = false;
    
    constructor(private auth:AuthService, private router: Router,private http: HttpClient ){
    
    }
    ngOnInit(){
      this.setPermissions();
    }
    
    logout(){
      this.auth.logout()
      this.router.navigate(['/login'])
    }
    onCourseChange(): void {
      
      const course = this.courses.find(c => c.course_name === this.selectedCourse);
      console.log(this.selectedCourse)
      if (course) {
        localStorage.setItem('course_key', course.course_key);  
      }
      this.course_key = ''
    }
    setPermissions(){
      this.auth.getRole().subscribe(role => {
        console.log('Role is:', role);
        this.student = role.toLowerCase() === 'student';
      this.instructor = role.toLowerCase() === 'instructor';
      console.log(this.instructor, this.student)

      //get courses for student or instructor
      if (this.instructor){
        this.get_courses_for_instructor();
        
      }
      if(this.student){
        this.get_courses_for_student();
      }
        
      });
     
    }
    create_course(){
      this.router.navigate(['/create-course'])
      
    }
    is_course_active(){
      return this.auth.getStorage()?.getItem("course_key")!==null
    }
    get_courses_for_instructor(){
      console.log('invoked')
      let token = this.auth.getStorage()?.getItem("access_token")
      if (!token){
        this.router.navigate(['/login']);
        return;
    }
      const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
      this.courses = [];
    this.http.get<any>('http://127.0.0.1:8000/api/instructor/courses/', {headers,observe: 'response' })
      .subscribe({
        next: (response) => {
          if(response.ok){
            let response_courses = response.body;
            console.log(response_courses)
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
    setCourseKey(event: Event){
      // event.preventDefault();
      this.show_course_key = true;
      this.course_key = this.auth.getStorage()?.getItem("course_key");

    }
    copyToClipBoard(){
      navigator.clipboard.writeText(this.course_key);
      this.course_icon = 'check_circle'
    }
    get_courses_for_student(){
      let token = this.auth.getStorage()?.getItem("access_token")
      if (!token){
        this.router.navigate(['/login']);
        return;
    }
      const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.get<any>('http://127.0.0.1:8000/api/student/courses/', {headers,observe: 'response' })
      .subscribe({
        next: (response) => {
          if(response.ok){
            let response_courses = response.body.enrolled_courses;
            console.log(response_courses)
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
