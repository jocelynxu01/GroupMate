import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../authorization.service';

@Component({
  selector: 'app-run-team-generator',
  imports: [],
  templateUrl: './run-team-generator.component.html',
  styleUrl: './run-team-generator.component.css'
})
export class RunTeamGeneratorComponent {
  constructor(private http: HttpClient, private auth: AuthService){}
  team_generator(){
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.auth.getAccessToken()}`);
    const body = {
      'course_key': this.auth.getCourseKey()
    }
    this.http.post<any>('http://127.0.0.1:8000/api/instructor/run-team-generator/', body,{headers,observe: 'response' })
      .subscribe({
        next: (response) => {
          if(response.ok){
            console.log('Successfully generated teams')
          
        }
      },
        error: (error) => {
          console.error('Teams generation endpoint couldnt complete', error);
         
        }
      });
  }
}
