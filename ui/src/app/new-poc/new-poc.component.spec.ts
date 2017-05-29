import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewPocComponent } from './new-poc.component';

describe('NewPocComponent', () => {
  let component: NewPocComponent;
  let fixture: ComponentFixture<NewPocComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewPocComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewPocComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
