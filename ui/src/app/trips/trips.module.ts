import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TripsComponent } from './trips/trips.component';
import { TripComponent } from './trip/trip.component';
import { NewTripComponent } from './new-trip/new-trip.component';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [
    TripsComponent,
    TripComponent,
    NewTripComponent
  ]
})
export class TripsModule { }
