import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { NgxMaskIonicModule } from 'ngx-mask-ionic';

import { SharedModule } from 'src/app/components/share.module';

import { RegisterPage } from 'src/app/pages/auth/register/register.page';

const routes: Routes = [
  {
    path: '',
    component: RegisterPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    IonicModule,
    RouterModule.forChild(routes),
    NgxMaskIonicModule,
    SharedModule
  ],
  declarations: [RegisterPage]
})
export class RegisterPageModule { }
