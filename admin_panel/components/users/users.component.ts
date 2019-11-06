import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { User } from '@app/_models';
import { LocalDataSource } from 'ng2-smart-table';
import { UserService, AuthenticationService, ChoicesService } from '@app/_services';
import { options } from '../../tables/Users';
import { HelperService } from '@app/_services/helper.service';



@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})

export class UsersComponent implements OnInit, OnDestroy {

  currentUser: User;
  currentUserSubscription: Subscription;
  isDataAvailable = false;
  users: User[] = [];
  usersAll: any = [];
  tempObj: any;
  langList: any = [];
  choices: any;
  source: LocalDataSource;
  settings = options;



  constructor(
    private authenticationService: AuthenticationService,
    private userService: UserService,
    private choicesService: ChoicesService,
    private helperService: HelperService
  ) {
    this.currentUserSubscription = this.authenticationService.currentUser.subscribe(user => {
      this.currentUser = user;
    });
    this.source = new LocalDataSource();
  }

  ngOnInit() {
    this.getSelectData();
    this.userService.deleting$.subscribe(() => {
      this.loadAllUsers();
    });
  }

  ngOnDestroy() {
    // unsubscribe to ensure no memory leaks
    this.currentUserSubscription.unsubscribe();
  }
  getSelectData() {
    this.choicesService.getChoices().subscribe((data: any) => {
      this.choices = data;

      for (const entry of this.choices.language) {
        this.langList.push({value: entry[1],title:  entry[1]} ); 
      }

      this.settings.columns.lang.filter.config.list = this.langList;
      this.source.refresh();
      this.loadAllUsers();
    });
  }
  loadAllUsers() {
    this.userService.getAllUsers().subscribe((data: any) => {
      this.usersAll = [];
      this.isDataAvailable = false;
      const users = data.content;

      for (const key in users) {
        if (users.hasOwnProperty(key)) {
          this.tempObj = {
            username: this.helperService.getProp(users[key], 'username'),
            email: this.helperService.getProp(users[key], 'email'),
            sim: this.helperService.getProp(users[key], 'profile', 'sim_number'),
            name: this.helperService.getProp(users[key], 'first_name'),
            phone: this.helperService.getProp(users[key], 'profile', 'phone'),
            lang: this.helperService.getProp(users[key], 'language_full'),
            requests: this.helperService.getProp(users[key], 'requests'),
            id: this.helperService.getProp(users[key], 'id'),
            role: this.helperService.getProp(users[key], 'role'),
          };
          this.usersAll.push(this.tempObj);
        }
      }

      this.source.load(this.usersAll);
      this.isDataAvailable = true;
    }, error => {
      this.source.load([]);
      this.isDataAvailable = true;
    });
  }

}
