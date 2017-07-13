import { Component, OnInit } from '@angular/core';

import { HttpService } from '../../shared/http.service';
import { Hour } from '../../shared/types';

@Component({
  selector: 'hour',
  templateUrl: './hour.component.html',
  styleUrls: ['./hour.component.css']
})
export class HourComponent implements OnInit {
  hourFields: Array<object>;
  constructor(private httpService: HttpService) { }

  ngOnInit() {
    this.httpService.getHourOptions().subscribe((options)=>{
      this.hourFields = options;
    });
  }

  saveHour = () => {
    let hourDetails = new Hour();
    hourDetails.newHour(this.hourFields);
    let convertedDetails = hourDetails.toHttp(hourDetails);
    this.httpService.saveHour(convertedDetails).subscribe(()=>{});
  }
}
