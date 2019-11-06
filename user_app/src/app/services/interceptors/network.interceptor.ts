import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { ToastController } from '@ionic/angular';
import { Network } from '@ionic-native/network/ngx';

import { Observable, throwError, from } from 'rxjs';
import { catchError, mergeMap } from 'rxjs/operators';

import { LanguageService } from 'src/app/services/language.service';

@Injectable()
export class NetworkInterceptor implements HttpInterceptor {

  private text: any;
  private toastIsPresent = false;

  private getPageText() {
    this.text = this.language.getTextByCategories();
  }

  private async showToast() {
    if (this.network.type === this.network.Connection.NONE && !this.toastIsPresent) {
      const toast = await this.toast.create({
        message: this.text ? this.text.disconnected : 'Missing connection to Internet!',
        duration: 2000
      });
      toast.present();
      this.toastIsPresent = true;
      toast.onDidDismiss().then(() => this.toastIsPresent = false);
    }
  }

  constructor(private toast: ToastController, private language: LanguageService, private network: Network) {
    this.language.languageIsLoaded$.subscribe(() => this.getPageText());
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return from(this.showToast()).pipe(
      mergeMap(() => next.handle(request).pipe(catchError(error => throwError(error))))
    );
  }
}
