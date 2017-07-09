import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';

import { Vessel, PortOfCall, Hour, Day, Note, CaseConverters } from './types';

@Injectable()
export class HttpService {
  url: string = 'http://127.0.0.1:8000/logbook/api/'

  constructor(private http: Http) {}

  getVessels(): Observable<Vessel[]> {
    return this.http.get(this.url+ 'vessels')
            .map(this.extractData);
  }

  getPorts(): Observable<PortOfCall[]> {
    return this.http.get(this.url+ 'portsofcall')
            .map(this.extractData);
  }

  getHours(): Observable<Hour[]> {
    return this.http.get(this.url + 'hours')
            .map(this.extractData);
  }

  getDays(): Observable<Hour[]> {
    return this.http.get(this.url + 'days')
            .map(this.extractData);
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
      var element = body.results[index];
      for(let key in element){
        newObj[converter.snakeToCamel(key)] = body.results[index][key];
      }
      newResults.push(newObj);
    }
    body.results = newResults;
    return body.results || { };
  }

}
