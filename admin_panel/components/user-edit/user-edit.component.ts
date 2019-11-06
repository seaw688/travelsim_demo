import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { first } from 'rxjs/operators';
import { Subscription } from 'rxjs';
import { User } from '@app/_models';
import { AlertService, UserService, AuthenticationService, ChoicesService } from '@app/_services';



@Component({
  selector: 'app-user-edit',
  templateUrl: './user-edit.component.html',
  styleUrls: ['./user-edit.component.css']
})

export class UserEditComponent implements OnInit {
    editForm: FormGroup;
    myForm: FormGroup;
    showFilter = false;
    loading = false;
    submitted = false;
    id: any;
    currentUser: User;
    currentUserSubscription: Subscription;
    user: object;
    isDataAvailable = false;
    edit = false;
    textSubmit = 'Create';
    langs: any = [];
    selectedItem: any = [];
    selectedItems: any = [];
    dropdownSettings: any = {};
    choices: any;




    constructor(
        private formBuilder: FormBuilder,
        private router: Router,
        private authenticationService: AuthenticationService,
        private userService: UserService,
        private alertService: AlertService,
        private route: ActivatedRoute,
        private choicesService: ChoicesService
    ) {
      this.currentUserSubscription = this.authenticationService.currentUser.subscribe(user => {
        this.currentUser = user;
      });
    }

    ngOnInit() {
      this.route.params.subscribe(params => {
        this.id = params['id'];
      });

      this.edit = this.id ? true : false;

      this.editForm = this.formBuilder.group({
          first_name: ['', Validators.required],
          email: ['', [Validators.required, Validators.email]],
          username: ['', Validators.required],
          last_name: ['', Validators.required],
          is_active: ['', Validators.required],
          role: ['', Validators.required],
          lang: ['', Validators.required],
          phone: ['', Validators.required],
          sim_number: [''],
          password: ['', Validators.compose([
            Validators.required,
            Validators.pattern('^(?=.*?[a-zA-Z])(?=.*?[0-9]).{8,}$')
          ])],
      });

      if (this.edit) {
        this.textSubmit = 'Update';
        this.getUser();
        this.editForm.get('password').clearValidators();
        this.editForm.get('password').updateValueAndValidity();
        this.editForm.removeControl('password');
      }
      this.getSelectData();
    }

    // convenience getter for easy access to form fields
    get f() { return this.editForm.controls; }

    onSubmit() {
        this.submitted = true;
        // stop here if form is invalid
        if (this.editForm.invalid) {
            return;
        }

        if (this.editForm.value.lang[0].item_id && this.editForm.value.lang[0].item_text) {
          this.editForm.addControl('language', new FormControl(''));
          this.editForm.get('language').setValue(this.editForm.value.lang[0].item_id);
          this.editForm.addControl('language_full', new FormControl(''));
          this.editForm.get('language_full').setValue(this.editForm.value.lang[0].item_text);
        }

        this.loading = true;
        this.edit ? this.updateUser() : this.registerUser();
    }

    updateUser() {
          this.userService.update(this.editForm.value, this.id)
          .pipe(first())
          .subscribe(
              data => {
                  this.alertService.success('Updated successful', true);
                  this.router.navigate(['/users']);
              },
              error => {
                  this.alertService.error(error);
                  this.loading = false;
              });
    }

    registerUser() {
      this.userService.register(this.editForm.value)
      .pipe(first())
      .subscribe(
          data => {
              this.alertService.success('Added successful', true);
              this.router.navigate(['/users']);
          },
          error => {
              if (error.error.email) {
                this.alertService.error(error.error.email);
              } else if (error.error.username)  {
                this.alertService.error(error.error.username);
              } else {
                this.alertService.error(error.statusText);
              }
              this.loading = false;
          }
        );
    }

    public getSelectData() {
      this.choicesService.getChoices().subscribe((data: any) => {
        this.choices = data;
        this.isDataAvailable = true;
        this.initMultiSelect();
      });
    }

    public initMultiSelect() {
      for (const entry of this.choices.language) {
        this.langs.push({
          item_id: entry[0],
          item_text: entry[1]
        });
      }

      this.dropdownSettings = {
        singleSelection: true,
        idField: 'item_id',
        textField: 'item_text',
        selectAllText: 'Select All',
        unSelectAllText: 'UnSelect All',
        itemsShowLimit: 2,
        allowSearchFilter: this.showFilter
      };

      if (!this.edit) {
        this.myForm = this.formBuilder.group({
          lang: ['']
        });
      }
    }

    private getUser() {
      this.userService.getById(this.id).subscribe((data: any) => {
        const user = data.content[0];
        this.user = user;
        this.isDataAvailable = true;

        this.setFormValues(user);
      });
    }

    public setFormValues(user: any) {
      this.editForm.get('first_name').setValue(user.first_name);
      this.editForm.get('username').setValue(user.username);
      this.editForm.get('email').setValue(user.email);
      this.editForm.get('last_name').setValue(user.last_name);
      this.editForm.get('is_active').setValue(user.is_active);
      this.editForm.get('role').setValue(user.role);
      this.selectedItem = [ {item_id: user.language, item_text: user.language_full }];
      this.myForm = this.formBuilder.group({
        lang: [this.selectedItems]
      });

      const phone = user.profile && user.profile.phone ? user.profile.phone : '';
      this.editForm.get('phone').setValue(phone);

      const sim = user.profile && user.profile.sim_number ? user.profile.sim_number : '';
      this.editForm.get('sim_number').setValue(sim);
    }
}
