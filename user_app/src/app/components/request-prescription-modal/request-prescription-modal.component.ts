import { Component, OnInit } from '@angular/core';

import { FormControl } from '@angular/forms';

import { ModalController, AlertController, Platform } from '@ionic/angular';
import { AndroidPermissions } from '@ionic-native/android-permissions/ngx';
import { InAppBrowser, InAppBrowserObject } from '@ionic-native/in-app-browser/ngx';

import { finalize } from 'rxjs/operators';

import { LanguageService } from 'src/app/services/language.service';
import { ImageService } from 'src/app/services/image.service';
import { LoadingService } from 'src/app/services/loading.service';
import { ApiService } from 'src/app/services/api.service';

import { Text, Image } from 'src/app/models/models';

@Component({
  selector: 'app-request-prescription-modal',
  templateUrl: './request-prescription-modal.component.html',
  styleUrls: ['./request-prescription-modal.component.scss']
})
export class RequestPrescriptionModalComponent implements OnInit {

  private messageFromBrowser: any = null;
  private modal: ModalController;
  private platform: string;
  private browser: InAppBrowserObject;
  private userId: number;
  private tranzilaCss = `
    #header, #footergreenstripe, #geo {
      display: none;
    }
    ul {
     margin-top: 30px;
    }
    li {
     height: 50px;
    }
    span, a, input, select {
      color: #7C8BFE;
    }
    input, select {
      height: 30px;
      background-color: #F2F6FC;
      border: 0 !important;
    }
    select {
      vertical-align: unset !important;
    }
    #send {
      margin-top: 20px;
    }
    #send button {
      width: 100%;
      border-radius: 0 !important;
      background: linear-gradient(to right, #6c9eff, #a25ffd) !important;
      height: 60px;
      margin-top: 30px;
    }
 `;

  public text: Text;
  public userComment: FormControl;
  public images: Image[] = [];

  constructor(
    private language: LanguageService,
    private image: ImageService,
    private loading: LoadingService,
    private api: ApiService,
    private alert: AlertController,
    private androidPermissions: AndroidPermissions,
    private ionicPlatform: Platform,
    private iab: InAppBrowser
  ) { }

  ngOnInit() {
    this.getPlatform();
    this.initFormControl();
  }

  ionViewWillEnter() {
    this.getPageText();
    this.getUserId();
  }

  private getPlatform() {
    this.platform = this.ionicPlatform.is('android') ? 'android' : 'ios';
  }

  private getPageText() {
    this.text = this.language.getTextByCategories('online_doctor_prescriptions');
  }

  private initFormControl() {
    this.userComment = new FormControl('');
  }

  private async showAlert(message: string) {
    const alert = await this.alert.create({
      message,
      buttons: [this.text.ok]
    });

    await alert.present();
    alert.onDidDismiss().then(() => this.modal.dismiss());
  }

  private async requestImageLibraryPermission() {
    const { hasPermission } = await this.androidPermissions.requestPermission(this.androidPermissions.PERMISSION.WRITE_EXTERNAL_STORAGE);
    if (hasPermission) {
      this.uploadImage();
    }
  }

  private getUserId() {
    this.api.getProfile().subscribe(({ content: { user_id } }) => this.userId = user_id);
  }

  public confirmPrescription(userId: number, productId: number, price: number) {
    this.browser = this.iab.create(
      // tslint:disable-next-line: max-line-length
      `https://direct.tranzila.com/diplomacy/newiframe.php?currency=1&tranmode=AK&payment_type=PRESCRIPTION-REQUEST&sum=${price}&user_id=${userId}&product_id=${productId}`,
      '_blank',
      { hideurlbar: 'yes', location: 'yes' }
    );
    this.browser.insertCSS({ code: this.tranzilaCss });
    if (this.platform === 'android') {
      this.browser.hide();
    }

    this.browser.on('loadstop').subscribe(async () => {
      await this.browser.insertCSS({ code: this.tranzilaCss });
      if (this.platform === 'android') {
        this.browser.show();
      }

      this.browser.executeScript({
        code: `
          localStorage.setItem('status', '');
          const button = document.getElementById('ok');
          button.addEventListener('click', () => localStorage.setItem('status', 'close'));
        `
      });
      if (this.platform === 'ios') {
        this.browser.executeScript({
          code: `
            document.addEventListener('touchend', (e) => {
              if (document.activeElement !== e.target) {
                document.activeElement.blur();
              }
           })
          `
        });
      }

      const interval = setInterval(async () => {
        const values: Array<any> = await this.browser.executeScript({ code: 'localStorage.getItem("status")' });
        this.messageFromBrowser = values[0];
        if (this.messageFromBrowser) {
          await this.browser.executeScript({ code: 'localStorage.setItem("status", "")' });
          clearInterval(interval);
          this.browser.close();
        }
      }, 300);
    });

    this.browser.on('exit').subscribe(() => {
      if (this.messageFromBrowser) {
        this.showAlert('Your prescriptions has been successfully created');
        console.log('browser closed');
      }
    });
  }

  public async uploadImage() {
    const { hasPermission } = await this.androidPermissions.checkPermission(this.androidPermissions.PERMISSION.WRITE_EXTERNAL_STORAGE);

    if (this.platform === 'ios' || (this.platform === 'android' && hasPermission)) {
      const image = await this.image.getPrescriptionImage();
      this.images.push(image);
      return;
    }

    this.requestImageLibraryPermission();

    // setTimeout(() => {
    //   const image = { src: "", file: null };
    //   this.images.push(image);
    // }, 2000);
  }

  public deleteImage(index: number) {
    this.images.splice(index, 1);
  }

  public closeModal() {
    this.modal.dismiss();
  }

  public submit() {
    const formData = new FormData();
    formData.append('user_comment', this.userComment.value);
    this.images.forEach((item, index) => formData.append(`photo_${index + 1}`, item.file, this.image.createImageName()));

    this.loading.createLoading(this.text.wait_please as string);
    this.api.createPrescription(formData)
      .pipe(finalize(() => this.loading.dismissLoading()))
      .subscribe(
        ({ content: { id, price } }) => {
          this.confirmPrescription(this.userId, id, price);
        },
        () => this.showAlert('An error has occurred, try again')
      );
  }
}
