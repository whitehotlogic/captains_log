import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CurrentTripComponent } from './current-trip.component';

describe('CurrentTripComponent', () => {
  let component: CurrentTripComponent;
  let fixture: ComponentFixture<CurrentTripComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CurrentTripComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CurrentTripComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
