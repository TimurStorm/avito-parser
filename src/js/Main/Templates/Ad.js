import { makeStyles } from '@material-ui/core/styles';
import newSolid from '@iconify-icons/clarity/new-solid';
import { Icon} from '@iconify/react';
import React from 'react';
import { connect } from 'react-redux';
import {async_eel_get_ad_info} from '../../Async/asyncActions';

const Ad = makeStyles({
    colors:{
      'main_color': '#223639',
      'font_color': '#dfdfdf',  
    },
    
    main: {
        backgroundColor: '#223639',
        minHeight: 30,
        width: '100%',
        border: '0 solid',
        borderRadius: 5,
        marginBottom: 5,
        cursor: 'pointer',
        display: 'inline-block',
        '&:hover': {
            background: '#2d474b',
        },
        
    },
    sign: {
        height: 20,
        width: 20,
        backgroundColor: '#26A18D',
        border: '0 solid',
        borderRadius: 5,
        float: 'left',
        margin: 5,
        marginRight: 10,
    },
    title: {
        fontSize: 13,
        
        
        marginTop: 7,
        marginLeft: 4,
    },
    price: {
        fontWeight: 'bold',
        marginTop: 6,
        marginLeft: 8,
        fontSize: 13,
        
    },
    new:{
        float: 'left',
        marginLeft: 10,
    }
});

function Componet(props) {
    const classes = Ad(props);

    let title = props.title;
    let price = props.price;
    let url = props.url;
    let nw = props.new;
    let parser = props.parser;

    let openAd = () => {
        props.getAdInfo(url, parser);
    };

    if (title.length > 26){
        title = title.slice(0, 20) + '...';
    }

    let nw_icon = null;

    if (nw) {nw_icon = <Icon icon={newSolid} style={{ fontSize: '30px' }}/>;}
    
    return <div className={classes.main} onClick={openAd}>
        <div className={classes.sign}></div>
        <div className={classes.title}>{title}</div>
        <div className={classes.new}>
            {nw_icon}
        </div>
        <div className={classes.price}>{price}</div>
    </div>  
}

let mapDispatchToProps = (dispatch) => {
    return {
        getAdInfo: (url, parser) => {
            dispatch(async_eel_get_ad_info(url, parser));
        },
    }
}

let ComponetConnect = connect(null,mapDispatchToProps)(Componet);

export default ComponetConnect;