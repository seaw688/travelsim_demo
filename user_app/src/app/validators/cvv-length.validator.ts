import { FormControl } from '@angular/forms';

import { Object } from 'src/app/models/models';

export class CvvLengthValidator {

  public static cvvLength(control: FormControl) {
    const errors: Object = {};

    if (control.value) {
      const value = control.value.toString();
      if (value.length > 0 && value.length < 3 || value.length > 3) {
        errors.length = true;
        return errors;
      }
      return null;
    }
    return null;
  }
}
