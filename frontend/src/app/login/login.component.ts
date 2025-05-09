import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../authorization.service';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, MatButtonModule, MatIconModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username = '';
  password = '';

  constructor(private http: HttpClient, private router: Router, private auth: AuthService) {}

  login(){
    const loginData = {
      username: this.username,
      password: this.password
    };
    this.http.post<any>('http://127.0.0.1:8000/login/', loginData)
      .subscribe({
        next: (response) => {
          
          localStorage.setItem("access_token",response.access);
          localStorage.setItem("refresh_token",response.refresh);
          
          this.router.navigate(['']);
          
        },
        error: (error) => {
          console.error('Login failed', error);
          alert('Username and password do not match, Check credentials');
          this.username = '';
          this.password = '';
        }
      });
      
  }
}
