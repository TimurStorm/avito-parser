import { Button, ButtonGroup} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import '../../../css/Scroll.css';
import Ad from './Ad';
import React, {useEffect} from 'react';
import { useSelector, useDispatch, shallowEqual, connect} from 'react-redux';
import {async_eel_get_all_parsers, async_eel_get_parser_ads} from '../../Async/asyncActions';



const Ads = makeStyles({
    colors:{
      'main_color': '#223639',
      'font_color': '#dfdfdf',  
    },   
    main: {
        backgroundColor: '#102326',
        height: 450,
        width:744,
        border: '0 solid',
        borderRadius: 5,
        padding: '24px 15px',
        fontFamily: 'Rubik',
        color: '#dfdfdf',
        float: 'left',
        marginRight: 16,
        
    },
    header:{
        fontSize: 20,
        fontWeight: 500,
    },
    filter:{
        height:60,
        margin: '5px 0px 5px 0px',
        display: 'inline-block',
        width: 600,
    },
    filts :{
        width: 300,
        marginBottom: 12,
        height:24,
    },
    label: {
        height: 24,
        fontSize: 14,
        fontWeight: 300,
        textTransform: 'none',
        marginRight: 10,
        float:'left'
    },
    view: {
        height:24,
        width:202,
        border: '0 solid',
        borderRadius: 5,
        backgroundColor: '#223639',
        float: 'right',
        
    },
    sort: {
        height:24,
        width:202,
        border: '0 solid',
        borderRadius: 5,
        backgroundColor: '#223639',
        float: 'right',
        display: 'inline',
        textAlign: 'middle',
        
    },
    group: {
        height: 24,
    },
    it: {
        width:101,
        color: '#dfdfdf',
        textTransform: 'none',
        border: '0 solid',
        borderRadius: 5,
    },
    ads: {
        marginTop: 22,
        height: 320,
        overflowY: 'scroll',
        width: 740,
    },
    
});

function Componet(props) {
    
    const classes = Ads(props);

    useEffect(() => {
        props.getParsers();
        props.getAds();
        setInterval(() => { props.getAds()}, 1500);
    },[])
    console.log(props);

    const ads = props.data.map((ad)=> <Ad 
        title={ad[0]} 
        price={ad[1]}
        parser={ad[2]} />);
    // TODO: ПОРЕШАТЬ ДАТУ НА ОБЪЕКТЫ ЧТОБЫ БЫЛИ ОБЪЯВЛЕНИЯ 
    return <div className={classes.main}>
        <div className={classes.header}>Объявления</div>
        <hr color={'#1b6259'} style={{marginBottom:4 , marginTop:16 }}/>
        <div className={classes.filter}>
            <div className={classes.filts}>
                <div className={classes.view}>
                <ButtonGroup className={classes.group} aria-label="outlined secondary button group">
                    <Button className={classes.it}>Строки</Button>
                    <Button className={classes.it}>Карточки</Button>
                </ButtonGroup>
                
                </div>
                <div className={classes.label} style={{paddingTop:3}}>
                    Вид:
                </div>
            </div>
            <div className={classes.filts} style={{margin: 0}}>
                <div className={classes.sort}>
                    <ButtonGroup className={classes.group} aria-label="outlined secondary button group">
                        <Button className={classes.it}>Новые</Button>
                        <Button className={classes.it}>Старые</Button>
                    </ButtonGroup>
                </div>
                <div className={classes.label}  style={{paddingTop:3}}>
                    Показывать:
                </div>
            </div>
        </div>
        <hr color={'#1b6259'} style={{marginTop:0 , marginBottom: 16}}/>
        <div className={classes.ads}>
            {ads}
        </div>
    </div>  
}

let mapStateToProps = (state) => {
    return {
        parsers: state.parsers,
        data: state.ads
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        getParsers: () => {
            dispatch(async_eel_get_all_parsers());
        },
        getAds: () => {
            dispatch(async_eel_get_parser_ads());
        }
    }
}

const ComponetConnect = connect(mapStateToProps, mapDispatchToProps)(Componet);

export default ComponetConnect;