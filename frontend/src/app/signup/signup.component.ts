import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  imports: [CommonModule, FormsModule],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})

export class SignupComponent {
  username = '';
  password = '';
  role=''
  email = '';
  first_name = '';
  last_name = '';

  constructor(private http: HttpClient, private router: Router) {}

  signup() {
    const register = {
      username: this.username,
      password: this.password,
      email: this.email,
      first_name: this.first_name,
      last_name: this.last_name,
      role: this.role
    };
    console.log(this.role)
    this.http.post<any>('http://127.0.0.1:8000/api/register/', register,{ observe: 'response' })
      .subscribe({
        next: (response) => {
          response.ok ? alert('Registration successful! You can now login') : alert('Registration failed!');
          this.router.navigate(['/login']);
        },
        error: (error) => {
          console.error('Sign Up failed', error);
          alert('Sign Up failed. ');
          console.log(error)
        }
      });
  }
}
