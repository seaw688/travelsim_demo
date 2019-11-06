import { FormControl } from '@angular/forms';
import * as _ from 'lodash';

export class PasswordValidator {

  public static password(control: FormControl) {
    const errors: any = {};
    if (control.value !== '') {
      if (!/.*[0-9].*/.test(control.value)) {
        errors.noDigits = true;
      }
      if (!/.*[a-z].*/.test(control.value)) {
        errors.noLowercase = true;
      }
      if (!/.*[A-Z].*/.test(control.value)) {
        errors.noUppercase = true;
      }
      if (!/^[a-zA-Z0-9]{8,}$/.test(control.value)) {
        errors.short = true;
      }
      if (_.size(errors) > 0) {
        return errors;
      }
      return null;
    }
    return null;
  }
}
