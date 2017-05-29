import { ActionReducer, Action } from '@ngrx/store';

import { ACTIONS } from './actions.types';

export enum CurrentViewState {
    home,
    day,
    hour,
    newpoc,
    newcrew,
    newvessel,
    vessels,
    vessel,
    newtrip,
    trips,
    trip,
    currenttrip
}

export interface ViewState {
    currentView: CurrentViewState;
}

export const initialState: ViewState = {
    currentView: CurrentViewState.home
}

export const view = (
    state: ViewState = initialState,
    action: Action): ViewState => {
    if(!action) {
        return state;
    }
    switch (action.type) {
        case ACTIONS.CHANGEVIEW:
            return Object.assign({}, state, { currentView: action.payload });
        default:
            return state;
    }
}
