import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { SharedModule } from 'src/app/components/share.module';

import { ChoosePlanPage } from 'src/app/pages/customer/choose-plan/choose-plan.page';

const routes: Routes = [
  {
    path: '',
    component: ChoosePlanPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes),
    SharedModule
  ],
  declarations: [ChoosePlanPage]
})
export class ChoosePlanPageModule { }
