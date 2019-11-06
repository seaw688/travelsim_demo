import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { StorageService } from 'src/app/services/storage.service';
import { ApiService } from 'src/app/services/api.service';
import { LanguageService } from 'src/app/services/language.service';

@Component({
  selector: 'app-alerts-and-notifications-start',
  templateUrl: './alerts-and-notifications-start.page.html',
  styleUrls: ['./alerts-and-notifications-start.page.scss'],
})
export class AlertsAndNotificationsStartPage {

  public text: any;

  constructor(
    private router: Router,
    private storage: StorageService,
    private api: ApiService,
    private language: LanguageService
  ) { }

  ionViewWillEnter() {
    this.getPageText();
  }

  private getPageText() {
    this.text = this.language.getTextByCategories('alerts_and_notifications_start');
  }

  public navigateTo(path: string) {
    this.router.navigateByUrl(path);
  }
}
