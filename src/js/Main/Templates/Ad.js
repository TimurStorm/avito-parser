import { makeStyles } from '@material-ui/core/styles';
import newSolid from '@iconify-icons/clarity/new-solid';
import { Icon} from '@iconify/react';
import React from 'react';

const Ad = makeStyles({
    colors:{
      'main_color': '#223639',
      'font_color': '#dfdfdf',  
    },
    
    main: {
        backgroundColor: '#223639',
        height: 30,
        width:  774 - 30 -35,
        border: '0 solid',
        borderRadius: 5,
        marginBottom: 5,
        display: 'inline-block',
        
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
        fontWeight: 500,
        float: 'left',
        marginTop: 7
    },
    price: {
        float: 'right',
        marginTop: 6,
        marginRight: 12,
    },
    new:{
        float: 'left',
        marginLeft: 10,
    }
});
  
export default function StyledComponents(props) {
    const classes = Ad(props);
    let title = props.title;
    let price = props.price;
    let nw = props.new;
    let like = props.like;
    let nw_icon = null;
    if (nw) {nw_icon = <Icon icon={newSolid} style={{ fontSize: '30px' }}/>;}
    
    return <div className={classes.main}>
        <div className={classes.sign}></div>
        <div className={classes.title}>{title}</div>
        <div className={classes.new}>
            {nw_icon}
        </div>
        <div className={classes.price}>{price}</div>
    </div>  
}