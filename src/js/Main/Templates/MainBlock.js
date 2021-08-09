import { Button, ButtonGroup} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import '../../../css/Scroll.css';
import Ad from './Ad';
import React from 'react';


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
//<Button className={classes.it}>Дешёвые</Button>
//<Button className={classes.it}>Дорогие</Button>
export default function StyledComponents(props) {
    const classes = Ads(props);
    let data = [
        {
            title: 'Toyota Supra 2004 года в почти идеальном состоянии, недорого',
            price: 5000,
            new: true,
        },
        {
            title: 'Toyota Camry',
            price: 4520,
            new: false,
        },
        {
            title: 'Toyota Rav4',
            price: 7600,
            new: false,
        },
        {
            title: 'Toyota Supra',
            price: 5000,
            new: false,
        },
        {
            title: 'Toyota Camry',
            price: 4520,
            new: false,
        },
        {
            title: 'Toyota Rav4',
            price: 7600,
            new: false,
        },
        {
            title: 'Toyota Supra',
            price: 5000,
            new: false,
        },
        {
            title: 'Toyota Camry',
            price: 4520,
            new: false,
        },
        {
            title: 'Toyota Rav4',
            price: 7600,
            new: false,
        },
        {
            title: 'Toyota Supra',
            price: 5000,
            new: false,
        },
        {
            title: 'Toyota Camry',
            price: 4520,
            new: false,
        },
        {
            title: 'Toyota Rav4',
            price: 7600,
            new: false,
        },
    ];
    let ads = data.map((ad)=> <Ad title={ad['title']} price={ad['price']} new={ad['new']} />);
    return <div className={classes.main}>
        <div className={classes.header}>Объявления</div>
        <hr color={'#1b6259'} style={{marginBottom:4 , marginTop: 16}}/>
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