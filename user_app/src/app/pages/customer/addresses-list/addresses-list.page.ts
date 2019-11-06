import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { ApiService } from 'src/app/services/api.service';
import { LanguageService } from 'src/app/services/language.service';

import { Address, BaseResponse } from 'src/app/models/models';

@Component({
  selector: 'app-addresses-list',
  templateUrl: './addresses-list.page.html',
  styleUrls: ['./addresses-list.page.scss'],
})
export class AddressesListPage {

  public addresses: Address[];
  public text: any;

  constructor(private router: Router, private api: ApiService, private language: LanguageService) { }

  ionViewWillEnter() {
    this.getAddressesList();
    this.getPageText();
  }

  private getAddressesList() {
    this.api.getAddressesList().subscribe((res: BaseResponse) => this.addresses = res.content);
  }

  private getPageText() {
    this.text = this.language.getTextByCategories('addresses_list');
  }

  public navigateTo(path: string) {
    this.router.navigateByUrl(`/${path}`);
  }
}
