import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule } from '@angular/router';
import { MaterialModule, MdButtonModule, MdToolbarModule, MdSidenavModule, MdTabsModule, MdGridListModule, MdInputModule } from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { LogModule } from './log/log.module';
import { TripsModule } from './trips/trips.module';
import { VesselsModule } from './vessels/vessels.module';

import { PipeModule } from './shared/pipe.module';
import { HttpService } from './shared/http.service';

import { AppComponent } from './app.component';
import { appRoutes } from './shared/app.routes';
import { NewCrewComponent } from './new-crew/new-crew.component';
import { NewPocComponent } from './new-poc/new-poc.component';


@NgModule({
  declarations: [
    AppComponent,
    NewCrewComponent,
    NewPocComponent
  ],
  imports: [
    LogModule,
    TripsModule,
    VesselsModule,
    BrowserModule,
    FormsModule,
    HttpModule,
    MaterialModule,
    MdButtonModule,
    MdToolbarModule,
    MdSidenavModule,
    MdTabsModule,
    MdGridListModule,
    MdInputModule,
    BrowserAnimationsModule,
    PipeModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [
    HttpService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
