import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MdTabsModule, MdCardModule, MdInputModule, MdButtonModule } from '@angular/material';

import { DynamicFormModule } from '../shared/dynamic-form/dynamic-form.module';
import { PipeModule } from '../shared/pipe.module';
import { NewVesselComponent } from './new-vessel/new-vessel.component';
import { VesselComponent } from './vessel/vessel.component';
import { VesselsComponent } from './vessels/vessels.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    DynamicFormModule,
    MdTabsModule,
    MdCardModule,
    MdInputModule,
    MdButtonModule,
    PipeModule
  ],
  declarations: [
    VesselsComponent,
    VesselComponent,
    NewVesselComponent
  ]
})
export class VesselsModule { }
