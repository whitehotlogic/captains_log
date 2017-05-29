import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewCrewComponent } from './new-crew.component';

describe('NewCrewComponent', () => {
  let component: NewCrewComponent;
  let fixture: ComponentFixture<NewCrewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewCrewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewCrewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
