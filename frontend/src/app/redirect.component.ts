import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './authorization.service';


@Component({
  selector: 'app-redirect',
  standalone: true,
  template: ''
})
export class RedirectComponent implements OnInit {
  constructor(private router: Router, private authService: AuthService) {}

  ngOnInit(): void {
  //   if (this.authService.isLoggedIn()) {
  //     this.router.navigate(['/home']);
  //   } else {
  //     this.router.navigate(['/login']);
  //   }
  // }
  }
}
