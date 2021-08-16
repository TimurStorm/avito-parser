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
    ads: []
}
const GET_PARSERS = 'GET_PARSERS';
const GET_ADS = 'GET_ADS';



const reducer = (state = defaultState, action) => {
    switch (action.type){
        case GET_PARSERS:
            return {...state, parsers: action.payload};
        case GET_ADS:
            return {...state, ads: action.payload};
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
