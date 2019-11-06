import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot, Router } from '@angular/router';

import { Observable, of } from 'rxjs';
import { switchMap } from 'rxjs/operators';

import { StorageService } from 'src/app/services/storage.service';

@Injectable({
  providedIn: 'root'
})
export class GuestGuard implements CanActivate {
  constructor(private storage: StorageService, private router: Router) { }

  canActivate(next: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
    return this.storage.get('token').pipe(
      switchMap(data => {
        const allowed = data ? false : true;
        if (!allowed) {
          this.router.navigateByUrl('/main');
        }
        return of(allowed);
      })
    );
  }
}
