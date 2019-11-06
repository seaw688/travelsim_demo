import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'phone'
})
export class PhoneNumberPipe implements PipeTransform {
  transform(value: any, args?: any): any {
    return value ? value.replace(/972/, '+972 ') : '';
  }
}
