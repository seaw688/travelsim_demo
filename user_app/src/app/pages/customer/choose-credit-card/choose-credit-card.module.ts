import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { SharedModule } from 'src/app/components/share.module';

import { ChooseCreditCardPage } from 'src/app/pages/customer/choose-credit-card/choose-credit-card.page';

const routes: Routes = [
  {
    path: '',
    component: ChooseCreditCardPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    IonicModule,
    RouterModule.forChild(routes),
    SharedModule
  ],
  declarations: [ChooseCreditCardPage]
})
export class ChooseCreditCardPageModule {}
