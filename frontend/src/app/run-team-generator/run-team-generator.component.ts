import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../authorization.service';
import { MatButtonModule } from '@angular/material/button';
import {MatProgressBarModule} from '@angular/material/progress-bar';
@Component({
  selector: 'app-run-team-generator',
  imports: [MatButtonModule, MatProgressBarModule],
  templateUrl: './run-team-generator.component.html',
  styleUrl: './run-team-generator.component.css'
})
export class RunTeamGeneratorComponent {
  constructor(private http: HttpClient, private auth: AuthService){}
  loading=false;
  team_generator(){
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.auth.getAccessToken()}`);
    const body = {
      'course_key': this.auth.getCourseKey()
    }
    this.loading=true;
    this.http.post<any>('http://127.0.0.1:8000/api/instructor/run-team-generator/', body,{headers,observe: 'response' })
      .subscribe({
        next: (response) => {
          if(response.ok){
            console.log('Successfully generated teams')
            setTimeout(() => {
              this.loading = false;
            }, 2000);
          
        }
      },
        error: (error) => {
          console.error('Teams generation endpoint couldnt complete', error);
         
        }
      });
    this.loading=false;
  }
}
