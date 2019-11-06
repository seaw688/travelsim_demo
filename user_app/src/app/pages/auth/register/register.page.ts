import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { MenuController } from '@ionic/angular';

import { from, forkJoin } from 'rxjs';
import { switchMap, finalize } from 'rxjs/operators';

import { ApiService } from 'src/app/services/api.service';
import { ImageService } from 'src/app/services/image.service';
import { StorageService } from 'src/app/services/storage.service';
import { LoadingService } from 'src/app/services/loading.service';
import { ActionSheetService } from 'src/app/services/action-sheet.service';
import { LanguageService } from 'src/app/services/language.service';
import { PushService } from 'src/app/services/push.service';

import { BaseResponse } from 'src/app/models/models';

import { PasswordValidator } from 'src/app/validators/password.validator';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage implements OnInit {

  public form: FormGroup;
  public text: any;
  public submitTry = false;

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private api: ApiService,
    private storage: StorageService,
    private loading: LoadingService,
    private menu: MenuController,
    private action: ActionSheetService,
    private language: LanguageService,
    private push: PushService,
    public image: ImageService,
  ) { }

  ngOnInit() {
    this.createForm();
    this.action.actionSheetDismissLanguage$
      .subscribe((res: { label: string, value: string }) => this.form.get('language').setValue(res.label));
  }

  ionViewWillEnter() {
    this.image.resetPhotoData();
    this.getPageText();
  }

  ionViewDidEnter() {
    this.menu.enable(false);
  }

  ionViewWillLeave() {
    this.menu.enable(true);
  }

  private getPageText() {
    this.text = this.language.getTextByCategories('registration');
  }

  private createForm() {
    this.form = this.formBuilder.group({
      first_name: ['', [Validators.required, Validators.pattern('^[\\S][a-zA-Z-]*$')]],
      last_name: ['', [Validators.required, Validators.pattern('^[\\S][a-zA-Z-]*$')]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, PasswordValidator.password]],
      confirm_password: ['', Validators.required],
      language: ['', Validators.required]
    });
  }

  private postTextData(): Promise<BaseResponse> {
    return new Promise((resolve, reject) => {
      const formData: FormData = new FormData();
      formData.append('first_name', this.form.get('first_name').value);
      formData.append('last_name', this.form.get('last_name').value);
      formData.append('email', this.form.get('email').value);
      formData.append('password', this.form.get('password').value);
      formData.append('language', this.action.language);
      this.api.register(formData).subscribe(
        res => resolve(res),
        err => reject(err)
      );
    });
  }

  private postImages() {
    return new Promise((resolve, reject) => {
      const formData: FormData = new FormData();
      if (this.image.imgInfo.profile.changed) {
        formData.append('photo', this.image.imgInfo.profile.file, this.image.createImageName());
      }
      if (this.image.imgInfo.airline.changed) {
        formData.append('airline_image', this.image.imgInfo.airline.file, this.image.createImageName());
      }
      if (this.image.imgInfo.travel.changed) {
        formData.append('travel_image', this.image.imgInfo.travel.file, this.image.createImageName());
      }
      if (this.image.imgInfo.passport.changed) {
        formData.append('passport_image', this.image.imgInfo.passport.file, this.image.createImageName());
      }
      if (this.image.imgInfo.medical.changed) {
        formData.append('medical_image', this.image.imgInfo.medical.file, this.image.createImageName());
      }

      this.api.postImages(formData).subscribe(
        res => resolve(res),
        err => reject(err)
      );
    });
  }

  public requireValidator(...fields: Array<string>): boolean {
    let valid = true;
    for (const field of fields) {
      if (this.form.get(field).hasError('required')) {
        valid = false;
        break;
      }
    }
    return !valid;
  }

  public async presentActionSheet() {
    await this.action.createLanguageActionSheet();
  }

  public async register() {
    this.submitTry = true;

    if (this.form.valid) {
      await this.loading.createLoading(this.text.registering);
      this.postTextData().then(
        res => {
          forkJoin(this.storage.set('token', res.content.token), this.storage.set('language', res.content.profile.language))
            .pipe(
              finalize(() => this.loading.dismissLoading()),
              switchMap(() => {
                this.push.registerDevicePush();
                return from(this.postImages());
              })
            )
            .subscribe(() => this.router.navigateByUrl('/main'));
        },
        err => {
          this.loading.dismissLoading();
          if (err.error.metadata.api_error_codes.includes(103)) {
            alert(this.text.user_exists_message);
            return;
          }
          alert('Error occured!');
        }
      );
    }
  }

  public navigate(url: string) {
    this.router.navigateByUrl(url);
  }
}
