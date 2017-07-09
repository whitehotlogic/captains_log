import { Component, OnInit, Input } from '@angular/core';

import { Vessel } from '../types';

@Component({
  selector: 'vessel',
  templateUrl: './vessel.component.html',
  styleUrls: ['./vessel.component.css']
})
export class VesselComponent implements OnInit {
  @Input() data: Vessel;

  constructor() { }

  ngOnInit() {
    console.log('data in vessel component', this.data);
  }

}
