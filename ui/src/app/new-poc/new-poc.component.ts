import { Component, OnInit } from '@angular/core';

import { HttpService } from '../shared/http.service';
import { PortOfCall } from '../shared/types';
import { QuestionControlService } from '../shared/dynamic-form/question-control.service';



@Component({
  selector: 'new-poc',
  templateUrl: './new-poc.component.html',
  styleUrls: ['./new-poc.component.css']
})
export class NewPocComponent implements OnInit {
  pocFields: any;
  constructor(private httpService: HttpService, private questionService: QuestionControlService) { }

  ngOnInit() {
    this.httpService.getPortOptions().subscribe((options)=>{
      this.pocFields = this.questionService.toQuestionBase(options);
      console.log(this.pocFields);
    });
  }

  saveVessel = () => {
    console.log('save poc',this.pocFields)
    let pocDetails = new PortOfCall();
    pocDetails.newPoc(this.pocFields);
    let convertedDetails = pocDetails.toHttp(pocDetails);
    console.log(convertedDetails);
    this.httpService.saveVessel(convertedDetails).subscribe(()=>{});
  }

}
