import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MdTabsModule, MdCardModule, MdInputModule, MdButtonModule } from '@angular/material';

import { CurrentTripComponent } from './current-trip/current-trip.component';
import { DayComponent } from './day/day.component';
import { HourComponent } from './hour/hour.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    MdTabsModule,
    MdCardModule,
    MdButtonModule,
    MdInputModule,
  ],
  declarations: [CurrentTripComponent, DayComponent, HourComponent]
})
export class LogModule { }
