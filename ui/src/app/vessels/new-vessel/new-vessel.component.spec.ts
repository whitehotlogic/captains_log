import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewVesselComponent } from './new-vessel.component';

describe('NewVesselComponent', () => {
  let component: NewVesselComponent;
  let fixture: ComponentFixture<NewVesselComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewVesselComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewVesselComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
