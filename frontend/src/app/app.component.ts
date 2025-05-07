import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AuthService } from './authorization.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Group Mate';
  constructor(private auth: AuthService, private router: Router){}

  
}
