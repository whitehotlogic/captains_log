import { Component, OnInit } from '@angular/core';

import { HttpService } from '../../shared/http.service';
import { Day } from '../../shared/types';

@Component({
  selector: 'day',
  templateUrl: './day.component.html',
  styleUrls: ['./day.component.css']
})
export class DayComponent implements OnInit {
  dayFields: Array<object>;
  constructor(private httpService: HttpService) { }

  ngOnInit() {
    this.httpService.getDayOptions().subscribe((options)=>{
      console.log(options)
      this.dayFields = options;
    });
  }

  saveCrew = () => {
    let dayDetails = new Day();
    dayDetails.newDay(this.dayFields);
    let convertedDetails = dayDetails.toHttp(dayDetails);
    this.httpService.saveDay(convertedDetails).subscribe(()=>{});
  }
}
