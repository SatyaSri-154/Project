import { Component } from '@angular/core';
import { UserService } from '../user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  
  loginData = { username: '', password: '' };
  registerData = { username: '', email: '', contact: '', address: '', password: '', confirmPassword: '' };
  registerMode = false;

  constructor(private userService: UserService, private router: Router) {}

  onLoginSubmit() {
    this.userService.login(this.loginData.username, this.loginData.password).subscribe(response => {
      if (response && response.status === 'success') {
        alert('Valid user');
        this.router.navigate(['/dashboard']);
      } else {
        alert('Invalid User');
      }
    }, error => {
      console.error('Login Error:', error);
      alert('Invalid user');
    });
  }

  onRegisterSubmit() {
    if (this.registerData.password !== this.registerData.confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    this.userService.register(this.registerData.username, this.registerData.email, this.registerData.contact, this.registerData.address, this.registerData.password, this.registerData.confirmPassword).subscribe(response => {
      if (response && response.status === 'success') {
        alert('Registration successful. Please login.');
        this.toggleRegisterMode();
      } else {
        alert('Registration failed: ' + response.message);
      }
    }, error => {
      console.error('Register Error:', error);
      alert('User already exists');
    });
  }

  toggleRegisterMode() {
    this.registerMode = !this.registerMode;
    if (!this.registerMode) {
      this.registerData = { username: '', email: '', contact: '', address: '', password: '', confirmPassword: '' };
    } else {
      this.loginData = { username: '', password: '' };
    }
  }
}