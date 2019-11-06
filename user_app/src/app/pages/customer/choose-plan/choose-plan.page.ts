import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { iif, EMPTY, of } from 'rxjs';
import { switchMap } from 'rxjs/operators';

import { ApiService } from 'src/app/services/api.service';
import { LanguageService } from 'src/app/services/language.service';
import { StorageService } from 'src/app/services/storage.service';

@Component({
  selector: 'app-choose-plan',
  templateUrl: './choose-plan.page.html',
  styleUrls: ['./choose-plan.page.scss'],
})
export class ChoosePlanPage implements OnInit {

  private companyId: string;

  public plans: Array<any>;
  public selectedPlanId: string;
  public text: any;
  public hideBage: boolean;
  public planIsSelected = false;
  public defaultHref = 'choose-company';

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private api: ApiService,
    private language: LanguageService,
    private storage: StorageService
  ) { }

  ngOnInit() {
    this.getCompanyId();
    this.getPlans();
  }

  ionViewWillEnter() {
    this.getPageText();
    this.defineHidingBages();
    this.deselectPlan();
  }

  private defineHidingBages(url: string = this.router.url) {
    this.hideBage = true;

    this.storage.get('token')
      .pipe(switchMap(res => iif(
        () => !!res,
        this.api.getMyPlan(),
        of(EMPTY)
      )))
      .subscribe(res => {
        if (res) {
          this.hideBage = false;
          this.defaultHref = 'my-plan';
        }
      });
    // this.api.getMyPlan().subscribe(res => {
    //   if (res) {
    //     this.hideBage = false;
    //     this.defaultHref = 'my-plan'
    //   }
    // });
  }

  private getPageText() {
    this.text = this.language.getTextByCategories('choose_plan');
  }

  private getCompanyId() {
    this.companyId = this.route.snapshot.params.companyId;
  }

  private getPlans() {
    this.api.getPlans(this.companyId).subscribe(res => this.plans = res.content);
  }

  private deselectPlan() {
    this.selectedPlanId = null;
    this.planIsSelected = false;
  }

  public navigateTo(to: string) {
    this.router.navigateByUrl(`/${to}`);
  }

  public selectPlan(id: string) {
    this.selectedPlanId = id;
    this.planIsSelected = true;
  }

  public navigateToEnterMobileNumber() {
    if (this.planIsSelected) {
      this.router.navigate(['/enter-mobile-number'], { queryParams: { companyId: this.companyId, planId: this.selectedPlanId } });
      // this.router.navigateByUrl(`/enter-mobile-number/${this.companyId}/${this.selectedPlanId}`);
    }
  }
}
