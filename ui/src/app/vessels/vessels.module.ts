import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MdTabsModule, MdCardModule, MdInputModule } from '@angular/material';

import { PipeModule } from '../shared/pipe.module';
import { VesselsComponent } from './vessels/vessels.component';
import { VesselComponent } from './vessel/vessel.component';
import { NewVesselComponent } from './new-vessel/new-vessel.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    MdTabsModule,
    MdCardModule,
    MdInputModule,
    PipeModule
  ],
  declarations: [
    VesselsComponent,
    VesselComponent,
    NewVesselComponent
  ]
})
export class VesselsModule { }
