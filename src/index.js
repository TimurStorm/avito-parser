import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './js/App';
import registerServiceWorker from './registerServiceWorker';
import {createStore, applyMiddleware} from 'redux';
import {Provider} from 'react-redux';
import {composeWithDevTools} from 'redux-devtools-extension';
import thunk from 'redux-thunk';

//action = {type: '' , payload: ''}

const defaultState = {
    parsers: [],
    ads: [],
    hrefs: [ '/favorite', '/settings','/profile']
}
const GET_PARSERS = 'GET_PARSERS';
const GET_ADS = 'GET_ADS';



const reducer = (state = defaultState, action) => {
    switch (action.type){
        case GET_PARSERS:

            if (action.payload.length != state.parsers.length){
                state = {...state, parsers: action.payload};
            }
            return {...state};
        case GET_ADS:

            if (action.payload.length != state.ads.length){
                state = {...state, ads: action.payload};
            }
            return {...state};
        default:
            return state;
    }
}

export const getParsersAction = (value) => ({type: GET_PARSERS, payload:value});
export const getAdsAction = (payload) => ({type: GET_ADS, payload});

const store = createStore(reducer, composeWithDevTools(applyMiddleware(thunk)));

ReactDOM.render(
<Provider store={store}>
    <App />
</Provider>
, document.getElementById('root'));
registerServiceWorker();
