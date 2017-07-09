import { Component, OnInit } from '@angular/core';

import { HttpService } from '../shared/http.service';
import { Crew } from '../shared/types';

@Component({
  selector: 'new-crew',
  templateUrl: './new-crew.component.html',
  styleUrls: ['./new-crew.component.css']
})
export class NewCrewComponent implements OnInit {
  crewFields: Array<object>;
  constructor(private httpService: HttpService) { }

  ngOnInit() {
    this.httpService.getCrewOptions().subscribe((options)=>{
      this.crewFields = options;
    });
  }

  saveCrew = () => {
    let crewDetails = new Crew();
    crewDetails.newCrew(this.crewFields);
    let convertedDetails = crewDetails.toHttp(crewDetails);
    this.httpService.saveCrew(convertedDetails).subscribe(()=>{});
  }


}
