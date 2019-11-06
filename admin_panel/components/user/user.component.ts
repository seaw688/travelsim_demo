import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import {  ActivatedRoute } from '@angular/router';
import { environment } from '@environments/environment';
import { User } from '@app/_models';
import { UserService, AuthenticationService } from '@app/_services';
import { HelperService } from '@app/_services/helper.service';




@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})

export class UserComponent implements OnInit {

  currentUser: User;
  currentUserSubscription: Subscription;
  id = 4;
  user: object;
  isDataAvailable = false;
  currentImage: string;
  url: string = environment.apiHost;
  showModal = false;



  constructor(
    private authenticationService: AuthenticationService,
    private userService: UserService,
    private route: ActivatedRoute,
    private helperService: HelperService
  ) {
      this.currentUserSubscription = this.authenticationService.currentUser.subscribe(user => {
          this.currentUser = user;
      });
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.id = params['id'];
      this.getUser();
    });
  }

  toggleModal = (image: string) => {
    this.showModal = !this.showModal;
    this.currentImage = image;
  }

  getUser() {
    this.userService.getById(this.id).subscribe((data: any) => {
      const user = data.content[0];

      this.user = {
        name : this.helperService.getProp(user, 'username'),
        email:  this.helperService.getProp(user, 'email'),
        lang: this.helperService.getProp(user, 'language'),
        username: this.helperService.getProp(user, 'first_name'),
        password: this.helperService.getProp(user, 'password'),
        sim:   this.helperService.getProp(user, 'profile', 'sim_number'),
        phone:  this.helperService.getProp(user, 'profile', 'phone'),
        photo : this.helperService.getProp(user, 'profile', 'photo'),
        airline_image : this.helperService.getProp(user, 'profile', 'airline_image'),
        travel_image : this.helperService.getProp(user, 'profile', 'travel_image'),
        passport_image: this.helperService.getProp(user, 'profile', 'passport_image'),
      };
      this.isDataAvailable = true;
    });
  }

}
