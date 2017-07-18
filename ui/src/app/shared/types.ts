

export class Vessel {
    id: number;
    name: string;
    model: string;
    manufacturer: string;
    length: number;
    draft: number;
    hullNumber: string;
    fuelCapacity: number;
    waterCapacity: number;
    batteryCapacity: number;
    engineManufacturer: string;
    engineNumber: string;
    engineType: string;
    ownerName: string;
    ownerCertificationAgency: string;
    ownerCertificationNumber: string;
    createdAt: string;
    updatedAt: string;
    
    constructor() {
    }

    newVessel = (formObj) => {
        for(let key in formObj){
            this[key] = formObj[key];
        }
    }

    toHttp = (params: Vessel) => {
        console.log(params)
        let converter = new CaseConverters();
        let postObj = {}
        for(let key in params){
            postObj[converter.camelToSnake(key)] = params[key];
        }
        return postObj;
    }
}

export class PortOfCall {
    name:string;
    latitude: number;
    longitude: number;
    notes?: string;
    createdAt: string;
    updatedAt: string;

    constructor(){}

    newPoc = (formObj) => {
        for(let key in formObj){
            this[key] = formObj[key];
        }
    }


    toHttp = (params: PortOfCall) => {
        let converter = new CaseConverters();
        let postObj = {}
        for(let key in params){
            postObj[converter.camelToSnake(key)] = params[key];
        }
    }
}

export class Day {
    vessel: Vessel;
    portOfCall: PortOfCall;
    date: string;
    totalDistanceThisDay: number;
    highTide: number;
    lowTide: number;
    skipper: string;
    createdAt: string;
    updatedAt: string;

    constructor(){}

    newDay = (formObj) => {
        for(let key in formObj){
            this[key] = formObj[key];
        }
    }

    toHttp = (params: Day) => {
        let converter = new CaseConverters();
        let postObj = {}
        for(let key in params){
            postObj[converter.camelToSnake(key)] = params[key];
        }
    }
}

export class Hour {
    day: Day;
    time: number;
    course: number
    speed: number
    latitude: number;
    longitude: number;
    weather: string;
    windSpeed: number;
    windDirection: number
    visibility: number
    engineHours: number;
    fuelLevel: number;
    waterLevel: number;
    distanceSinceLastEntry: number;
    timezone?: string;
    createdAt: string;
    updatedAt: string;

    constructor(){
    }

    newHour = (formObj) => {
        for(let key in formObj){
            this[key] = formObj[key];
        }
    }

    toHttp = (params: Hour) => {
        let converter = new CaseConverters();
        let postObj = {}
        for(let key in params){
            postObj[converter.camelToSnake(key)] = params[key];
        }
    }
}

export class Note {
    timestamp: string;
    vessel: Vessel;
    note: string;
    createdAt: string;
    updatedAt: string;

    constructor(){}

    toHttp = (params: Note) => {
        let converter = new CaseConverters();
        let postObj = {}
        for(let key in params){
            postObj[converter.camelToSnake(key)] = params[key];
        }
    }
}

export class User {

}

export class Crew {
    id: string;
    crewName: string;
    crewUser: User;
    canSkipper: boolean;
    isActive: boolean;
    createdBy: User;
    updatedBy: User;
    createdAt: string;
    updatedAt: string;

    constructor(){
        this.isActive = false;
        this.canSkipper = false;
    }

    newCrew = (formObj) => {
        for(let key in formObj){
            this[key] = formObj[key];
        }
    }

    toHttp = (params: Crew) => {
        let converter = new CaseConverters();
        let postObj = {}
        for(let key in params){
            postObj[converter.camelToSnake(key)] = params[key];
        }
        return postObj;
    }
}

export class Trip {
    id: string;
    trip_name: string;
    vessels: Array<Vessel>;
    start_date: string;
    end_date: string;
    starting_port: Array<PortOfCall>;
    crew: Array<Crew>;
    stops: PortOfCall;
    destination_port: PortOfCall;
    created_by: User;
    updated_by: User;
    created_at: string;
    updated_at: string;
    history: Array<Trip>;

    constructor(){}

    newTrip = (formObj) => {
        for(let key in formObj){
            this[key] = formObj[key];
        }
    }

    toHttp = (params: Trip) => {
        let converter = new CaseConverters();
        let postObj = {}
        for(let key in params){
            postObj[converter.camelToSnake(key)] = params[key];
        }
    }
}


export class CaseConverters {
    public snakeToCamel = (word) =>{
        return word.replace(/(\_\w)/g, function(matched){return matched[1].toUpperCase();});
    }
    public camelToSnake = (word) => {
        return word.replace(/([a-z])([A-Z])/g, '$1_$2').toLowerCase();
    }
    public camelToCapital = (word) => {
        let newWord = word.replace(/([a-z])([A-Z])/g, '$1 $2');
        return newWord.charAt(0).toUpperCase() + newWord.slice(1);
    }
}