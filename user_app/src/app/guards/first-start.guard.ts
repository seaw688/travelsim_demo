import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot, Router } from '@angular/router';

import { Observable, of } from 'rxjs';
import { switchMap, catchError } from 'rxjs/operators';

import { StorageService } from 'src/app/services/storage.service';

@Injectable({
  providedIn: 'root'
})
export class FirstStartGuard implements CanActivate {

  constructor(private storage: StorageService, private router: Router) { }

  canActivate(next: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> | boolean {
    if (next.fragment) {
      return true;
    }
    return this.storage.get('not_first_launch')
      .pipe(
        switchMap(res => {
          const allowed = res ? false : true;
          if (!allowed) {
            this.router.navigateByUrl('/main');
          }
          return this.storage.set('not_first_launch', 'true').pipe(switchMap(() => of(allowed)));
        }),
        catchError(() => {
          return of(true);
        })
      );
  }
}
