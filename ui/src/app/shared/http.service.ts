import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';

import { Vessel, PortOfCall, Hour, Day, Note, CaseConverters, Crew, Trip } from './types';

@Injectable()
export class HttpService {
  url: string = 'http://localhost:4200/logbook/api/'
  headers: Headers;
  constructor(private http: Http) {
      this.headers = new Headers();  //*******
      this.headers.append('Content-Type', 'application/json') //******
  }

  getVessels(): Observable<Vessel[]> {
    return this.http.get(this.url+ 'vessels/')
      .map(this.extractData);
  }
  
  getVesselOptions(){
    return this.http.options(this.url + 'vessels/')
      .map(this.extractOptions);
  }

  saveVessel(vesselDetails): Observable<Response> {
    return this.http.post(this.url +'vessels/', vesselDetails);
  }

  getTrips(): Observable<Trip[]> {
    return this.http.get(this.url+ 'trips/')
      .map(this.extractData);
  }
  
  getTripOptions(){
    return this.http.options(this.url + 'trips/')
      .map(this.extractOptions);
  }

  saveTrip(tripDetails): Observable<Response> {
    return this.http.post(this.url +'trips/', tripDetails);
  }

  getPorts(): Observable<PortOfCall[]> {
    return this.http.get(this.url+  'portsofcall/')
      .map(this.extractData);
  }

  getPortOptions(){
    return this.http.options(this.url + 'portsofcall/')
      .map(this.extractOptions);
  }

  savePort(portDetails): Observable<Response> {
    return this.http.post(this.url + 'portsofcall/', portDetails);
  }

  getCrew(): Observable<Crew> {
    return this.http.get(this.url + 'crew/')
      .map(this.extractData);
  }

  getCrewOptions(){
    return this.http.options(this.url + 'crew/')
      .map(this.extractOptions);
  }

  saveCrew(crewDetails): Observable<Response> {
    return this.http.post(this.url + 'crew/', crewDetails);
  }

  getHours(): Observable<Hour[]> {
    return this.http.get(this.url + 'hours/')
      .map(this.extractData);
  }

  getHourOptions(){
    return this.http.options(this.url + 'hours/')
      .map(this.extractOptions);
  }

  saveHour(hourDetails): Observable<Response> {
    return this.http.post(this.url + 'hours/', hourDetails);
  }

  getDays(): Observable<Hour[]> {
    return this.http.get(this.url + 'days/')
      .map(this.extractData);
  }

  getDayOptions() {
    return this.http.options(this.url + 'days/')
      .map(this.extractOptions);
  }

  saveDay(dayDetails): Observable<Response> {
    return this.http.post(this.url + 'days/', dayDetails);
  }

  getNotes(): Observable<Note[]> {
    return this.http.get(this.url + 'notes')
      .map(this.extractData);
  }

  fromHttp(params) {
  }

  private extractData(res: Response) {
    let body = res.json();
    let converter = new CaseConverters();
    let newResults = [];
    for (var index = 0; index < body.results.length; index++) {
      let newObj = {};
      let element = body.results[index];
      for(let key in element){
        newObj[converter.snakeToCamel(key)] = body.results[index][key];
      }
      newResults.push(newObj);
    }
    body.results = newResults;
    return body.results || { };
  }

  private extractOptions(res: Response) {
    let body = res.json();
    let converter = new CaseConverters();
    let element = body.actions.POST;
    let fields = [];
    for(let key in element){
      let fieldsObj = {}
      let newKey = converter.snakeToCamel(key);
      fieldsObj = body.actions.POST[key];
      fieldsObj['readOnly'] = fieldsObj['read_only'];
      fieldsObj['field'] = newKey
      fieldsObj['value'] = '';
      fields.push(fieldsObj);
    }
    return fields;
  }

}
