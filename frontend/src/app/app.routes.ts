import { Routes } from '@angular/router';
import { SignupComponent } from './signup/signup.component';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { CreateCourseComponent } from './create-course/create-course.component';
import { JoinCourseComponent } from './join-course/join-course.component';
import { FillDetailsComponent } from './fill-details/fill-details.component';
import { ViewTeamMembersComponent } from './view-team-members/view-team-members.component';
import { RunTeamGeneratorComponent } from './run-team-generator/run-team-generator.component';
import { ViewClassMembersComponent } from './view-class-members/view-class-members.component';
import { ClassFeedComponent } from './class-feed/class-feed.component';
export const routes: Routes = [
  
  { path: 'signup', component: SignupComponent },
  { path: 'login', component: LoginComponent },

  
  { 
    path: '', 
    component: HomeComponent,
    children: [
      { path: 'create-course', component: CreateCourseComponent},
      

  { path: 'student/join-class', component: JoinCourseComponent},
  { path: 'student/fill-details', component: FillDetailsComponent},
  { path: 'student/view-team', component: ViewTeamMembersComponent},
  {path:'instructor/generate',component: RunTeamGeneratorComponent},
  {path:'view-class-members', component: ViewClassMembersComponent},
  {path:'view-class-feed', component: ClassFeedComponent}
    ]
  },



];
