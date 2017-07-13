import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MdTabsModule, MdCardModule, MdInputModule, MdButtonModule } from '@angular/material';


import { DynamicFormModule } from '../shared/dynamic-form/dynamic-form.module';
import { CurrentTripComponent } from './current-trip/current-trip.component';
import { DayComponent } from './day/day.component';
import { HourComponent } from './hour/hour.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    DynamicFormModule,
    MdTabsModule,
    MdCardModule,
    MdButtonModule,
    MdInputModule,
  ],
  declarations: [
    CurrentTripComponent,
    DayComponent,
    HourComponent
  ]
})
export class LogModule { }
