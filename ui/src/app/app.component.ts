import { Component } from '@angular/core';

import { HttpService } from './http.service';
import { Vessel } from './types';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app works!';
  vessels: Array<Vessel>;

  constructor(private httpService: HttpService){
    httpService.getVessels().subscribe((vessels) => {
      this.vessels = vessels;
      console.log(vessels);
    });
  }
}
