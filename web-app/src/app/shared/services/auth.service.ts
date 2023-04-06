import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthResponse, User, UserLoginData, UserRegisterData } from '../../auth/model/auth.model';
import { BehaviorSubject } from 'rxjs';
import { map } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  public user$: BehaviorSubject<User | null> = new BehaviorSubject<User | null>(null);

  constructor(private httpClient: HttpClient, private router: Router) {
    this.user$.next(JSON.parse(localStorage.getItem('user')!));
  }

  public login(user: UserLoginData, image: File) {
    const formData = new FormData();
    formData.append('user', JSON.stringify(user));
    formData.append('image', image, image.name);

    return this.httpClient
      .post<AuthResponse>('http://localhost:8080/api/auth/login', formData)
      .pipe(
        map((response) => {
          localStorage.setItem('token', response.token);
          const user: User = response;
          localStorage.setItem('user', JSON.stringify(user));
          this.user$.next(user);
        })
      );
  }

  public register(user: UserRegisterData, images: File[]) {
    const formData = new FormData()
    formData.append('register_data', JSON.stringify(user));
    images.forEach(img => formData.append('images', img));
    return this.httpClient
      .post<AuthResponse>('http://localhost:8080/api/auth/register', formData)
      .pipe(
        map((response) => {
          localStorage.setItem('token', response.token);
          const user: User = response;
          localStorage.setItem('user', JSON.stringify(user));
          this.user$.next(user);
        })
      );
  }

  public getToken(): string | null {
    const token = localStorage.getItem('token');
    if (token) {
      const payload = token.split('.')[1];
      const decodedPayload = atob(payload);
      const tokenPayload = JSON.parse(decodedPayload);
      const expirationTime = tokenPayload.exp * 1000;
      const isTokenExpired = expirationTime < Date.now();

      return isTokenExpired ? null : token;
    }
    return null;
  }

  public isLoggedIn(): boolean {
    return this.user$.value !== null && this.getToken() != null;
  }

  public logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    this.user$.next(null);
    this.router.navigate(['/auth/login']);
  }
}
