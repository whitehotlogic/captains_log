import { ActionReducer, Action } from '@ngrx/store';

import { ACTIONS } from './actions.types';
import { Vessel } from './types';


export enum VesselTabs {
    details,
    supply,
    pastTrips,
    currentTrip,

}

export class VesselStore {
    currentVessel: Vessel;
    vessels: Array<Vessel>;
    currentVesselTab: VesselTabs;
}

export const initialVesselState: VesselStore = {
    currentVessel: null,
    vessels: [],
    currentVesselTab: VesselTabs.details
}

export const vesselStore = (
    state: VesselStore = initialVesselState,
    action: Action): VesselStore => {
    if(!action){
        return state;
    }
    switch (action.type) {
        case ACTIONS.ADDVESSEL:
            return Object.assign({}, state, {
                currentVessel: action.payload,
                currentVesselTab: VesselTabs.details,
                vessels: state.vessels.push(action.payload)
            });
        case ACTIONS.SETCURRENTVESSEL:
            return Object.assign({}, state, {
                currentVessel: action.payload,
                currentVesselTab: VesselTabs.details,
                vessels: state.vessels
            });
    }
}
