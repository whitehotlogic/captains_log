import { combineReducers } from '@ngrx/store';
import { compose } from  '@ngrx/core/compose';

import { ViewState, view } from './view.reducer';
import { VesselStore, vesselStore } from './vessel.reducer';
// import { TripStore, tripStore } from './trip.reducer';
// import { LogStore, logStore } from './log.reducer';


export interface AppState {
    View: ViewState;
    Vessels: VesselStore;
    // Trips: TripStore;
    // Log: LogStore;
}

// export function appState(){
//     return compose(combineReducers)({
//         View: ViewState,
//         Vessels: VesselStore,
//         Trips: TripStore,
//         Log: LogStore
//     });
// }

export const appState = combineReducers({
    View: view,
    Vessels: vesselStore,
    // Trips: tripStore,
    // Log: logStore
});
