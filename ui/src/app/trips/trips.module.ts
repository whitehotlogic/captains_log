import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MdTabsModule, MdCardModule, MdInputModule, MdButtonModule } from '@angular/material';

import { DynamicFormModule } from '../shared/dynamic-form/dynamic-form.module';
import { PipeModule } from '../shared/pipe.module';
import { NewTripComponent } from './new-trip/new-trip.component';
import { TripComponent } from './trip/trip.component';
import { TripsComponent } from './trips/trips.component';


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    MdTabsModule,
    MdCardModule,
    MdInputModule,
    MdButtonModule,
    PipeModule,
    DynamicFormModule
  ],
  declarations: [
    TripsComponent,
    TripComponent,
    NewTripComponent
  ]
})
export class TripsModule { }
