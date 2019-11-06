import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { SharedModule } from 'src/app/components/share.module';

import { AlertsAndNotificationsStartPage } from 'src/app/pages/customer/alerts-and-notifications-start/alerts-and-notifications-start.page';

const routes: Routes = [
  {
    path: '',
    component: AlertsAndNotificationsStartPage
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
  declarations: [AlertsAndNotificationsStartPage]
})
export class AlertsAndNotificationsStartPageModule {}
