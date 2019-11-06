import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { SharedModule } from 'src/app/components/share.module';

import { AddressesListPage } from 'src/app/pages/customer/addresses-list/addresses-list.page';

const routes: Routes = [
  {
    path: '',
    component: AddressesListPage
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
  declarations: [AddressesListPage]
})
export class AddressesListPageModule {}
