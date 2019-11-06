import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RequestPrescriptionModalComponent } from './request-prescription-modal.component';

describe('RequestPrescriptionModalComponent', () => {
  let component: RequestPrescriptionModalComponent;
  let fixture: ComponentFixture<RequestPrescriptionModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RequestPrescriptionModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RequestPrescriptionModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
