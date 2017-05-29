import { Component, OnInit } from '@angular/core';

import { HttpService } from '../../shared/http.service';
import { Vessel } from '../../shared/types';

@Component({
  selector: 'new-vessel',
  templateUrl: './new-vessel.component.html',
  styleUrls: ['./new-vessel.component.css']
})
export class NewVesselComponent implements OnInit {

  boatFields: Array<object>;
  constructor(private httpService: HttpService) { }

  ngOnInit() {
    this.boatFields = [{
        field: 'name',
        label: 'Name',
        value: ''
      },{
        field: 'manufacturer',
        label: 'Manufacturer',
        value: ''
      },{
        field: 'length',
        label: 'Length',
        value: ''
      },{
        field: 'draft',
        label: 'Draft',
        value: ''
      },{
        field: 'model',
        label: 'Model',
        value: ''
      },{
        field: 'hullNumber',
        label: 'Hull Number',
        value: ''
      },{
        field: 'fuelCapacity',
        label: 'Fuel Capacity',
        value: ''
      },{
        field: 'waterCapacity',
        label: 'Water Capacity',
        value: ''
      },{
        field: 'batteryCapacity',
        label: 'Battery Capacity',
        value: ''
      },{
        field: 'engineManufacturer',
        label: 'Engine Manufacturer',
        value: ''
      },{
        field: 'engineNumber',
        label: 'Engine Number',
        value: ''
      },{
        field: 'engineType',
        label: 'Engine Type',
        value: ''
      },{
        field: 'ownerName',
        label: 'Owner Name',
        value: ''
      },{
        field: 'ownerCertificationAgency',
        label: 'Owner Certification Agency',
        value: ''
      },{
        field: 'ownerCertificationNumber',
        label: 'Owner Certification Number',
        value: ''
    }]
  }

  saveVessel = () => {
    console.log('save vessel',this.boatFields)
    let boatDetails = new Vessel();
    boatDetails.newVessel(this.boatFields);
    let convertedDetails = boatDetails.toHttp(boatDetails);
    console.log(convertedDetails)
    this.httpService.saveVessel(convertedDetails).subscribe(()=>{});
  }

}
