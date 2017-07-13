import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule, MdButtonModule, MdToolbarModule, MdSidenavModule, MdTabsModule, MdGridListModule, MdInputModule } from '@angular/material';

import { DynamicFormQuestionComponent } from './dynamic-form-question.component';
import { DynamicFormComponent } from './dynamic-form.component';
import { QuestionControlService } from './question-control.service';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    MaterialModule,
    MdButtonModule,
    MdInputModule,
    ReactiveFormsModule
  ],
  declarations: [
    DynamicFormQuestionComponent,
    DynamicFormComponent
  ],
  exports: [
    DynamicFormComponent
  ],
  providers: [
    QuestionControlService
  ]
})
export class DynamicFormModule { }
