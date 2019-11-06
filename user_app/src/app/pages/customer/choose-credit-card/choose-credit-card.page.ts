import { Component, OnInit, OnDestroy, AfterViewInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';

import { AlertController } from '@ionic/angular';

import { Subscription } from 'rxjs';
import { finalize, switchMap } from 'rxjs/operators';

import { LanguageService } from 'src/app/services/language.service';
import { ActionSheetService } from 'src/app/services/action-sheet.service';
import { LoadingService } from 'src/app/services/loading.service';
import { ApiService } from 'src/app/services/api.service';

import { CvvLengthValidator } from 'src/app/validators/cvv-length.validator';

import { SimPlan } from 'src/app/models/models';

@Component({
  selector: 'app-choose-credit-card',
  templateUrl: './choose-credit-card.page.html',
  styleUrls: ['./choose-credit-card.page.scss'],
})
export class ChooseCreditCardPage implements OnInit, OnDestroy, AfterViewInit {

  private actionSubscription: Subscription;
  private creditCardId: number;

  public queryParams: { planId?: string, companyId?: string } = {};
  public text: any;
  public form: FormGroup;
  public submitTry = false;

  constructor(
    private language: LanguageService,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    private action: ActionSheetService,
    private loading: LoadingService,
    private api: ApiService,
    private alert: AlertController,
    private router: Router
  ) { }

  ngOnInit() {
    this.createForm();

    this.actionSubscription = this.action.actionSheetDismissCreditCard$.subscribe((res: { label: string, value: number }) => {
      this.form.get('credit_card').setValue(res.label);
      this.creditCardId = res.value;
    });
  }

  ngAfterViewInit() {
    this.form.get('credit_card').valueChanges.subscribe(() => {
      this.form.get('cvv').setValue(null);
    });
  }

  ngOnDestroy() {
    this.unsubscribe();
  }

  ionViewWillEnter() {
    this.getPageText();
    this.getQueryParams();
  }

  private navigateTo(navigateTo: string) {
    this.router.navigateByUrl(`/${navigateTo}`);
  }

  private unsubscribe() {
    if (this.actionSubscription) {
      this.actionSubscription.unsubscribe();
    }
  }

  private createForm() {
    this.form = this.formBuilder.group({
      credit_card: ['', Validators.required],
      cvv: [null, [Validators.required, CvvLengthValidator.cvvLength, Validators.pattern('^\\d*$')]]
    });
  }

  private getQueryParams() {
    this.route.queryParamMap.subscribe(params => {
      this.queryParams.planId = params.get('planId');
      this.queryParams.companyId = params.get('companyId');
    });
  }

  private getPageText() {
    this.text = this.language.getTextByCategories();
  }

  private async createAlert(success: boolean): Promise<HTMLIonAlertElement> {
    const message = success ? 'The transaction completed successfully!' : this.text.unknown_error;
    const alert = await this.alert.create({
      message,
      buttons: [this.text.ok]
    });
    await alert.present();

    return alert;
  }

  public async presentActionSheet() {
    await this.action.createCreditCardActionSheet();
  }

  public async buySimCard() {
    this.submitTry = true;

    if (this.form.valid) {
      let successBuying = true;

      await this.loading.createLoading(this.text.wait_please);

      this.api.getPlan(this.queryParams.planId)
        .pipe(
          switchMap(({ content: { price } }) => {
            const requestBody: SimPlan = {
              card: this.creditCardId,
              pack: parseInt(this.queryParams.planId, 10),
              price: parseInt(price, 10),
              cvv: this.form.get('cvv').value
            };

            return this.api.buySimPlan(requestBody).pipe(finalize(async () => {
              await this.loading.dismissLoading();

              const alert = await this.createAlert(successBuying);
              await alert.onDidDismiss();

              if (successBuying) {
                this.navigateTo('main');
              }
            }));
          })
        )
        .subscribe(
          () => { },
          () => successBuying = false
        );
    }
  }
}
