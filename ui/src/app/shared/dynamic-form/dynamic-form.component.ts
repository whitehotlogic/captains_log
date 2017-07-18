import { Component, Input, OnInit, Output, EventEmitter }  from '@angular/core';
import { FormGroup }                 from '@angular/forms';
 
import { QuestionBase }              from './question-base.types';
import { QuestionControlService }    from './question-control.service';
 
@Component({
  selector: 'dynamic-form',
  templateUrl: './dynamic-form.component.html',
  providers: [ QuestionControlService ]
})
export class DynamicFormComponent implements OnInit {
 
  @Output() formSubmit = new EventEmitter<any>();
  @Input() questions: QuestionBase<any>[] = [];
  form: FormGroup;
  payLoad = '';
 
  constructor(private qcs: QuestionControlService) {  }
 
  ngOnInit() {
    this.form = this.qcs.toFormGroup(this.questions);
  }
 
  onSubmit() {
    this.payLoad = JSON.stringify(this.form.value);
    this.formSubmit.emit(this.form.value);
  }
}