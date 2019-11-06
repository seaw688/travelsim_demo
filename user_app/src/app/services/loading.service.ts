import { Injectable } from '@angular/core';
import { LoadingController } from '@ionic/angular';

@Injectable({
  providedIn: 'root'
})
export class LoadingService {

  private loading: any;

  constructor(private loadingController: LoadingController) { }

  public async createLoading(message: string = 'Wait, please') {
    this.loading = await this.loadingController.create({
      message: message,
      spinner: 'dots'
    });
    return this.loading.present();
  }

  public async dismissLoading() {
    await this.loading.dismiss();
  }
}
