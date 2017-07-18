import { Component, OnInit } from '@angular/core';

import { HttpService } from '../shared/http.service';
import { Crew } from '../shared/types';
import { QuestionControlService } from '../shared/dynamic-form/question-control.service';

@Component({
  selector: 'new-crew',
  templateUrl: './new-crew.component.html',
  styleUrls: ['./new-crew.component.css']
})
export class NewCrewComponent implements OnInit {
  crewFields: Array<object>;
  constructor(private httpService: HttpService, private questionService: QuestionControlService) { }

  ngOnInit() {
    this.httpService.getCrewOptions().subscribe((options)=>{
      this.crewFields = this.questionService.toQuestionBase(options);
    });
  }

  onSubmit(formData) {
    let crewDetails = new Crew();
    crewDetails.newCrew(formData);
    let convertedDetails = crewDetails.toHttp(crewDetails);
    this.httpService.saveCrew(convertedDetails).subscribe(()=>{});
  }


}
