import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { HttpService } from '../../shared/http.service';
import { Trip } from '../../shared/types';

@Component({
  selector: 'app-trips',
  templateUrl: './trips.component.html',
  styleUrls: ['./trips.component.css']
})
export class TripsComponent implements OnInit {
  
  trips: Array<Trip>;

  constructor(
  private router: Router,
  private httpService: HttpService) {
    httpService.getTrips().subscribe((trips) => {
      this.trips = trips;
      console.log(trips);
    });
  }

  ngOnInit() {
  }
  onSelect(trip: Trip) {
    this.router.navigate(['/trip', trip.id]);
  }

  newTrip() {
    this.router.navigate(['/new-trip']);
  }

}
