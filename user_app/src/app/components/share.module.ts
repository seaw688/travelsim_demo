import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { HeaderComponent } from 'src/app/components/header/header.component';
import { NoDataMessageComponent } from 'src/app/components/no-data-message/no-data-message.component';
import { RequestPrescriptionModalComponent } from './request-prescription-modal/request-prescription-modal.component';

import { PhoneNumberPipe } from 'src/app/pipes/phone-number.pipe';

@NgModule({
  imports: [
    CommonModule,
    IonicModule,
    ReactiveFormsModule
  ],
  declarations: [HeaderComponent, PhoneNumberPipe, NoDataMessageComponent, RequestPrescriptionModalComponent],
  exports: [HeaderComponent, PhoneNumberPipe, NoDataMessageComponent],
  entryComponents: [RequestPrescriptionModalComponent]
})
export class SharedModule { }
