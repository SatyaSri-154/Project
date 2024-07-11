import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private baseUrl = 'http://localhost:5000';  // Update with your Flask server URL
  private currentUser: string | null;

  constructor(private http: HttpClient, private router: Router) {
    this.currentUser = localStorage.getItem('currentUser');
  }

  login(username: string, password: string) {
    return this.http.post<any>(`${this.baseUrl}/login`, { username, password })
     .pipe(
        tap((response: any) => {
          this.setCurrentUser(username);
        })
      );
  }

  register(username: string, email: string, contact: string, address: string, password: string, confirmPassword: string) {
    const userData = { username, email, contact, address, password, confirmPassword };
    return this.http.post<any>(`${this.baseUrl}/register`, userData);
  }

  setCurrentUser(username: string): void {
    localStorage.setItem('currentUser', username); // Store username in localStorage
    this.currentUser = username;
  }

  getCurrentUser(): string | null {
    return this.currentUser; // This will return either a string or null
  }

  isLoggedIn(): boolean {
    return this.currentUser!== null;
  }
  

  logout(): void {
    localStorage.removeItem('currentUser');
    this.currentUser = null;
    this.router.navigate(['/']);
  }
}