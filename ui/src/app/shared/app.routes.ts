import { Routes } from '@angular/router';

import { VesselsComponent } from '../vessels/vessels/vessels.component';
import { VesselComponent } from '../vessels/vessel/vessel.component';
import { NewVesselComponent } from '../vessels/new-vessel/new-vessel.component';

import { TripsComponent } from '../trips/trips/trips.component';
import { TripComponent } from '../trips/trip/trip.component';
import { NewTripComponent } from '../trips/new-trip/new-trip.component';

import { DayComponent } from '../log/day/day.component';
import { HourComponent } from '../log/hour/hour.component';

import { NewCrewComponent } from '../new-crew/new-crew.component';
import { NewPocComponent } from '../new-poc/new-poc.component';


export const appRoutes: Routes = [
  { path: 'vessels', component: VesselsComponent },
  { path: 'vessel/:id', component: VesselComponent },
  { path: 'new-vessel', component: NewVesselComponent },
  { path: 'trips', component: TripsComponent },
  { path: 'current-trip', component: TripComponent },
  { path: 'new-trip', component: NewTripComponent },
  { path: 'day', component: DayComponent },
  { path: 'hour', component: HourComponent },
  { path: 'new-crew', component: NewCrewComponent },
  { path: 'new-poc', component: NewPocComponent },
  { path: 'new-vessel', component: NewVesselComponent }
];