import { Component } from '@angular/core';
import { AuthService } from '../authorization.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-home',
  imports: [CommonModule, FormsModule, RouterOutlet],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
    instructor = false;
    student = false;

    constructor(private auth:AuthService, private router: Router){
      
    }
    ngOnInit(){
      this.setPermissions();
    }
    logout(){
      this.auth.logout()
      this.router.navigate(['/login'])
    }
    setPermissions(){
      this.auth.getRole().subscribe(role => {
        console.log('Role is:', role);
        this.student = role.toLowerCase() === 'student';
      this.instructor = role.toLowerCase() === 'instructor';
      console.log(this.instructor, this.student)
        
      });
     
    }
    create_course(){
      
      this.router.navigate(['/create-course'])
    }

}
