import { HttpClient, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { Observable, throwError } from 'rxjs';
import { mergeMap, catchError } from 'rxjs/operators';
import * as _ from 'lodash';

import { ApiService } from 'src/app/services/api.service';
import { StorageService } from 'src/app/services/storage.service';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {
  private http: HttpClient;

  constructor(
    private apiService: ApiService,
    private router: Router,
    private storage: StorageService
  ) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return this.apiService.getToken().pipe(
      mergeMap(token => {
        const newRequest = token
          ? request.clone({ url: request.url + '/', setHeaders: { Authorization: `Token ${token}` } })
          : request.clone({ url: request.url + '/' });
        if (!token) {
          if (this.router.url.includes('register')) {
            this.router.navigateByUrl('/register');
          }
          if (this.router.url.includes('login')) {
            this.router.navigateByUrl('/login');
          }
          if (this.router.url.includes('forgot-password')) {
            this.router.navigateByUrl('/forgot-password');
          }
        }
        return next.handle(newRequest).pipe(
          catchError(error => {
            if ([119, 401].includes(error.status)) {
              this.storage.remove('token').subscribe(() => this.router.navigateByUrl('/login'));
            }
            return throwError(error);
          })
        );
      })
    );
  }
}
