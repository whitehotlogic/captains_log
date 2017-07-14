import { Component, OnInit } from '@angular/core';

import { HttpService } from '../../shared/http.service';
import { Trip } from '../../shared/types';
import { QuestionControlService } from '../../shared/dynamic-form/question-control.service';

@Component({
  selector: 'new-trip',
  templateUrl: './new-trip.component.html',
  styleUrls: ['./new-trip.component.css']
})
export class NewTripComponent implements OnInit {

  tripFields: Array<object>;
  constructor(private httpService: HttpService, private questionService: QuestionControlService) { }

  ngOnInit() {
    this.httpService.getTripOptions().subscribe((options)=>{
      this.tripFields = this.questionService.toQuestionBase(options);
      console.log(this.tripFields)
    });
  }

  saveTrip = () => {
    console.log('save vessel',this.tripFields)
    let tripDetails = new Trip();
    tripDetails.newTrip(this.tripFields);
    let convertedDetails = tripDetails.toHttp(tripDetails);
    console.log(convertedDetails)
    this.httpService.saveTrip(convertedDetails).subscribe(()=>{});
  }

}
