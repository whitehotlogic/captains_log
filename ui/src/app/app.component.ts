import { Component } from '@angular/core';

import { HttpService } from './shared/http.service';
import { Vessel } from './shared/types';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  vessels: Array<Vessel>;

  constructor(private httpService: HttpService){
    httpService.getVessels().subscribe((vessels) => {
      this.vessels = vessels;
    });
  }
}
