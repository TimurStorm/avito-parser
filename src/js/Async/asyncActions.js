import {getParsersAction, getAdsAction, getAdInfoAction} from '../../index'

const eel = window["eel"];

export function async_eel_get_all_parsers() {
    return function (dispatch) {
        eel.get_all_parsers()().then(value => dispatch(getParsersAction(value)));
    };
}

export function async_eel_get_parser_ads() {
    return function (dispatch) {
        eel.get_parser_ads()().then(value => dispatch(getAdsAction(value)));
    };
}

export function async_eel_get_ad_info(url, parser) {
    return function (dispatch) {
        eel.get_ad_info(url, parser)().then(value => dispatch(getAdInfoAction(value)));
    };
}