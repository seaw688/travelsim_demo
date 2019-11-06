import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

import { Subscription, forkJoin } from 'rxjs';
import { switchMap, filter, tap } from 'rxjs/operators';

import { ApiService } from 'src/app/services/api.service';
import { StorageService } from 'src/app/services/storage.service';
import { LanguageService } from 'src/app/services/language.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit, OnDestroy {

  private navigationSubscription: Subscription;
  private languageSubscription: Subscription;

  @Input() public showBackBtn = false;
  @Input() public defaultHref?: string;
  @Input() public backBtnText?: string;
  @Input() public queryParams = null;

  public hideBage = true;
  public isAuthorized: boolean;
  public text: any;

  constructor(
    private router: Router,
    private storage: StorageService,
    private api: ApiService,
    private language: LanguageService
  ) {
    this.storage.get('token').subscribe(res => {
      res ? this.isAuthorized = true : this.isAuthorized = false;
    });
  }

  ngOnInit() {
    this.getPageText();

    this.languageSubscription = this.language.languageIsLoaded$.subscribe(() => this.getPageText());

    this.navigationSubscription = this.router.events
      .pipe(
        filter(e => e instanceof NavigationEnd)
      )
      .subscribe(() => this.getPageText());
  }

  ngOnDestroy() {
    this.navigationSubscription.unsubscribe();
    this.languageSubscription.unsubscribe();
  }

  private getPageText() {
    this.text = this.language.getTextByCategories('menu');
  }

  public navigateTo(to: string) {
    if (to !== '') {
      this.router.navigate([`/${to}`], { queryParams: this.queryParams });
      return;
    }
    this.router.navigate(['/']);
  }

  public logout() {
    this.storage.get('auth_type')
      .pipe(
        tap(async (res: string) => {
          if (res === 'GOOGLE') {
            await this.api.googleLogout();
          }
          if (res === 'FACEBOOK') {
            await this.api.facebookLogout();
          }
        }),
        switchMap(() => this.api.logout().pipe(
          switchMap(() => forkJoin(this.storage.remove('token'), this.storage.remove('profile'), this.storage.remove('auth_type')))
        ))
      )
      .subscribe(() => this.navigateTo('login'));
  }
}
