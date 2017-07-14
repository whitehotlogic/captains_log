import { Component, OnInit } from '@angular/core';

import { HttpService } from '../../shared/http.service';
import { Vessel } from '../../shared/types';
import { QuestionControlService } from '../../shared/dynamic-form/question-control.service';

@Component({
  selector: 'new-vessel',
  templateUrl: './new-vessel.component.html',
  styleUrls: ['./new-vessel.component.css']
})
export class NewVesselComponent implements OnInit {

  boatFields: Array<object>;
  constructor(private httpService: HttpService, private questionService: QuestionControlService) { }

  ngOnInit() {
    this.httpService.getVesselOptions().subscribe((options)=>{
      this.boatFields = this.questionService.toQuestionBase(options);
      console.log(this.boatFields)
    });
  }

  saveVessel = () => {
    console.log('save vessel',this.boatFields)
    let boatDetails = new Vessel();
    boatDetails.newVessel(this.boatFields);
    let convertedDetails = boatDetails.toHttp(boatDetails);
    console.log(convertedDetails)
    this.httpService.saveVessel(convertedDetails).subscribe(()=>{});
  }

}
