import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { KeysPipe } from './keys.pipe';
import { AppComponent } from './app.component';
import { HttpService } from './http.service';
import { VesselComponent } from './vessel/vessel.component';

@NgModule({
  declarations: [
    AppComponent,
    VesselComponent,
    KeysPipe
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [HttpService],
  bootstrap: [AppComponent]
})
export class AppModule { }
