import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ChoosePlanPage } from './choose-plan.page';

describe('ChoosePlanPage', () => {
  let component: ChoosePlanPage;
  let fixture: ComponentFixture<ChoosePlanPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ChoosePlanPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ChoosePlanPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
