import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddressesListPage } from './addresses-list.page';

describe('AddressesListPage', () => {
  let component: AddressesListPage;
  let fixture: ComponentFixture<AddressesListPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddressesListPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddressesListPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
