import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CurrentTripComponent } from './current-trip/current-trip.component';
import { DayComponent } from './day/day.component';
import { HourComponent } from './hour/hour.component';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [CurrentTripComponent, DayComponent, HourComponent]
})
export class LogModule { }
