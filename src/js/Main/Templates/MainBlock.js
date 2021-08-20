import { makeStyles , createTheme} from '@material-ui/core/styles';
import React from 'react';
import {connect} from 'react-redux';
import { Button , Grid} from '@material-ui/core';

const Ads = makeStyles({
    colors:{
      'main_color': '#223639',
      'font_color': '#dfdfdf',  
    },   
    main: {
        backgroundColor: '#102326',
        width:'0%',
        minWidth: 270,
        height: 505,
        border: '0 solid',
        borderRadius: 5,
        padding: '24px 15px',
        fontFamily: 'Rubik',
        color: '#dfdfdf',
        float: 'left',
        margin:16,
        marginTop: 32,
    },
    header:{
        fontSize: 20,
        fontWeight: 400,
        marginBottom: 10,
    },
    desc:{
        marginTop: 25,
        fontSize: 12,
        
        height:120,
        fontWeight: 300,
        overflowY: 'auto',
    },
    price:{
        marginTop:15,
    },
    btn:{
        textTransform: 'none',
        backgroundColor: '#26A18D',
        paddingLeft: 66,
        paddingRight: 66,
        marginTop: 25,
        '&:hover': {
          backgroundColor: '#239481',
        },
      }
    });
    
    function Componet(props){
    const classes = Ads(props);
    let img;
    let desc;
    let title;
    let price;
    let date;
    console.log(props.adinfo);
    if (props.adinfo){
        img = props.adinfo['img'];
        desc = props.adinfo['desc'];
        title = props.adinfo['title'];
        price = props.adinfo['price'];
    }
    
    return <Grid item lg={8} md={8} sm={8}  xs={8} className={classes.main}>
        {props.adinfo &&
            <div>
                <div className={classes.header}>{title}</div>
                <div className={classes.img}><img src={img[0]} height='180' width='240'/></div>
                <div className={classes.price}>Цена:{price}</div>
                <div className={classes.desc}>{desc}</div>
                <Button className={classes.btn}>Подробнее</Button>
            </div>
        }
        {!props.adinfo &&
            <div>
                <div className={classes.desc}>ggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggssssssssssssssssssssssssssssss</div>
            </div>
        }
    </Grid>
    }
    
    let mapStateToProps = (state) => {
    return {
        adinfo: state.adinfo,
    }
    }
    
    
    const ComponetConnect = connect(mapStateToProps)(Componet);

export default ComponetConnect;


