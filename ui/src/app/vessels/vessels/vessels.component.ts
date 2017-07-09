import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { HttpService } from '../../shared/http.service';
import { Vessel } from '../../shared/types';


@Component({
  selector: 'vessels',
  templateUrl: './vessels.component.html',
  styleUrls: ['./vessels.component.css']
})
export class VesselsComponent implements OnInit {
  
  vessels: Array<Vessel>;

  constructor(
  private router: Router,
  private httpService: HttpService){
    httpService.getVessels().subscribe((vessels) => {
      this.vessels = vessels;
      console.log(vessels);
    });
  }

  ngOnInit() {
  }
  onSelect(vessel: Vessel) {
    this.router.navigate(['/vessel', vessel.id]);
  }
  newVessel(){
    this.router.navigate(['/new-vessel'])
  }

}
