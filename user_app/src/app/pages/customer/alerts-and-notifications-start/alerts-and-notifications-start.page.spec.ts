import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlertsAndNotificationsStartPage } from './alerts-and-notifications-start.page';

describe('AlertsAndNotificationsStartPage', () => {
  let component: AlertsAndNotificationsStartPage;
  let fixture: ComponentFixture<AlertsAndNotificationsStartPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AlertsAndNotificationsStartPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlertsAndNotificationsStartPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
