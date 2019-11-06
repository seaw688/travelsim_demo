import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot } from '@angular/router';

import { ToastController } from '@ionic/angular';
import { Network } from '@ionic-native/network/ngx';

import { StorageService } from 'src/app/services/storage.service';
import { LanguageService } from 'src/app/services/language.service';

@Injectable({
  providedIn: 'root'
})
export class NetworkGuard implements CanActivate {

  private text: any;

  constructor(
    private storage: StorageService,
    private network: Network,
    private toast: ToastController,
    private language: LanguageService
  ) {
    this.language.languageIsLoaded$.subscribe(() => this.getPageText());
  }

  canActivate(next: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (this.network.type === this.network.Connection.NONE) {
      this.showToast();
      return false;
    }
    return true;
  }

  private getPageText() {
    this.text = this.language.getTextByCategories();
  }

  private async showToast() {
    const toast = await this.toast.create({
      message: this.text ? this.text.disconnected : 'Missing connection to Internet!',
      duration: 2000
    });
    toast.present();
  }
}
