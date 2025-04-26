import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { jwtDecode } from 'jwt-decode';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { isPlatformBrowser } from '@angular/common';

interface JwtPayload {
  exp: number; 
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(
    private http: HttpClient, 
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}
  
  private getStorage(): Storage | null {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage;
    }
    return null;
  }
  getCourseKey(){
    return this.getStorage()?.getItem("course_key");
  }
  getAccessToken(){
    return this.getStorage()?.getItem("access_token");
  }
  getRefreshToken(){
    return this.getStorage()?.getItem("refresh_token");
  }

  getRole(): Observable<string> {
    const storage = this.getStorage();
    const token = storage?.getItem("access_token");
    if (!token) {
      return of('');
    }
  
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
  
    return this.http.get<any>('http://127.0.0.1:8000/api/getrole/', { headers }).pipe(
      map(response => response.role || ''),
      catchError(() => of(''))
    );
  }

  logout(): void {
    this.getStorage()?.removeItem('access_token');
    this.getStorage()?.removeItem('refresh_token');
    this.getStorage()?.removeItem('course_key');
  }

  refresh_token(token: any): Observable<boolean> {
    const body = {
      "refresh": token
    };
    
    return this.http.post<any>('http://127.0.0.1:8000/api/token/refresh/', body, { observe: 'response' }).pipe(
      map(response => {
        if (response.ok) {
          const access_token = response.body.access;
          this.getStorage()?.setItem("access_token", access_token);
          return true;
        }
        return false;
      }),
      catchError(error => {
        console.error('Refresh Failed', error);
        return of(false);
      })
    );
  }
}