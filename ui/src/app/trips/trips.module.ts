import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MdTabsModule, MdCardModule, MdInputModule, MdButtonModule } from '@angular/material';

import { PipeModule } from '../shared/pipe.module';
import { TripsComponent } from './trips/trips.component';
import { TripComponent } from './trip/trip.component';
import { NewTripComponent } from './new-trip/new-trip.component';


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    MdTabsModule,
    MdCardModule,
    MdInputModule,
    MdButtonModule,
    PipeModule
  ],
  declarations: [
    TripsComponent,
    TripComponent,
    NewTripComponent
  ]
})
export class TripsModule { }
