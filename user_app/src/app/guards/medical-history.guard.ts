import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot, Router } from '@angular/router';

import { Observable, of, iif } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';

import { ApiService } from 'src/app/services/api.service';
import { StorageService } from 'src/app/services/storage.service';

@Injectable({
  providedIn: 'root'
})
export class MedicalHistoryGuard implements CanActivate {

  constructor(private router: Router, private api: ApiService, private storage: StorageService) { }

  canActivate(next: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
    return this.storage.get('token')
      .pipe(switchMap(res => iif(
        () => !!res,
        this.api.checkMedicalHistory()
          .pipe(
            catchError(() => {
              this.router.navigateByUrl('/medical-history');
              return of(false);
            }),
            switchMap(() => of(true))
          ),
        of(true)
      )));
  }
}
