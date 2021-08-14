import {eel} from '../eel';
import {getParsersAction, getAdsAction} from '../../index'


export function async_eel_get_all_parsers() {
    return function (dispatch) {
        eel.get_all_parsers()().then(value => dispatch(getParsersAction(value)));
    };
}
export function async_eel_get_parser_ads(parser) {
    return function (dispatch) {
        eel.get_parser_ads(parser)().then(value => dispatch(getAdsAction(value)));
    };
}