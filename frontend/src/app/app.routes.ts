import { Routes } from '@angular/router';
import { SignupComponent } from './signup/signup.component';
import { LoginComponent } from './login/login.component';
import { ListClassesInstructorComponent } from './list-classes-instructor/list-classes-instructor.component';
import { HomeComponent } from './home/home.component';
import { RedirectComponent } from './redirect.component';
import { CreateCourseComponent } from './create-course/create-course.component';
import { JoinCourseComponent } from './join-course/join-course.component';
import { ListClassesStudentComponent } from './list-classes-student/list-classes-student.component';
import { FillDetailsComponent } from './fill-details/fill-details.component';
import { ViewTeamMembersComponent } from './view-team-members/view-team-members.component';
export const routes: Routes = [
  
  { path: 'signup', component: SignupComponent },
  { path: 'login', component: LoginComponent },

  
  { 
    path: '', 
    component: HomeComponent,
    children: [
      { path: 'create-course', component: CreateCourseComponent},
  { path: 'instructor/get-class', component: ListClassesInstructorComponent},
  { path: 'student/join-class', component: JoinCourseComponent},
  { path: 'student/get-classes', component: ListClassesStudentComponent},
  { path: 'student/fill-details', component: FillDetailsComponent},
  { path: 'student/view-team', component: ViewTeamMembersComponent}
    ]
  },



];
