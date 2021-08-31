import { makeStyles } from '@material-ui/core/styles';
import React, {useState, useEffect} from 'react';
import { Icon} from '@iconify/react';
import {connect} from 'react-redux';
import { Button , Grid,} from '@material-ui/core';
import closeOutline  from '@iconify-icons/eva/close-outline';

var lexample = true;

const Ads = makeStyles({
    colors: {
      'main_color': '#223639',
      'font_color': '#dfdfdf',  
    },   
    main: {
        backgroundColor: '#102326',
        minWidth: 353,
        height: 623,
        border: '0 solid',
        borderRadius: 5,
        padding: "24px 16px",
        fontFamily: 'Rubik',
        color: '#dfdfdf',
        float: 'left',
        margin:16,
        marginTop: 32,
    },
    header:{
        fontFamily: 'sans-serif',
        fontSize: 20,
        fontWeight: 400,
        marginBottom: 10,
    },
    desc:{
        marginTop: 8,
        fontSize: 12,
        fontWeight: 300,
    },
    price:{
        marginTop:8,
        display: 'inline-block',
    },
    date:{
        display: 'inline-block',
        marginLeft: 15,
        fontSize: 13,
        color: 'grey',
    },
    btn:{
        textTransform: 'none',
        backgroundColor: '#26A18D',
        paddingLeft: 66,
        paddingRight: 66,
        marginTop: 16,
        marginBottom: 16,
        '&:hover': {
          backgroundColor: '#239481',
        },
    },
    error_title:{
        fontSize:35,
        fontWeight:400,
    },
    error_info:{
        margintTop:35,
        fontWeight:200,
    },
    close:{
        float: 'right',
        cursor: 'pointer',
    },
    address:{
        fontSize: 14,
        fontWeight: 200,
        marginTop: 8,
    },
    params:{
        marginTop: 8,
        fontSize: 13,
        fontWeight: 300,
    },
    param_item:{
        backgroundColor: '#223639',
        border: '0 solid',
        borderRadius: 5,
        marginBottom:5,
        marginRight:5,
        paddingLeft:10,
        paddingTop:5,
        minHeight: 24,
        width: '98%',
        verticalAlign: 'bottom',
    },
    scroll_cont:{
        height: 497,
        overflowY: 'auto',
    },
    data_header:{
        fontSize:15,
        fontWeight:400,
        marginTop:16,
    },
    img_cont:{
        display: 'inline-block',
    },
    img_item:{
        marginBottom:16,
    },
    img_image:{
        '&:hover': {
            filter: 'brightness(60%)',
        },
        '&:active': {
            filter: 'brightness(50%)',
        },
    },
    img_big:{
        display: 'inline-block',
        height: 360,
        width:480,
        backgroundColor: '#0d1c1f',
        textAlign: 'center',
        marginTop: 16
    }
    });
    
    function Componet(props){
    const classes = Ads(props);
    const [bigImg, setImg] = useState(0);
    const [new_title, setTitle] = useState(0);



    let img;
    let desc;
    let title;
    let price;
    let date;
    let address;
    let params;
    let url;

    console.log(props.adinfo);
    if (props.adinfo){
        title = props.adinfo['title'];
        if (new_title != title){
            setTitle(title);
            lexample = true;
        }
        url = props.adinfo['url'];
        img = props.adinfo['img'];
        if (bigImg != img[0] && lexample){
            setImg(img[0]);
            lexample = false;
        }
        desc = props.adinfo['desc'];
        price = props.adinfo['price'];
        date = props.adinfo['date'];
        address = props.adinfo['address'];
        params = props.adinfo['params'];
    }

    return <Grid item lg={8} md={8} sm={8}  xs={8} className={classes.main}>
        {props.adinfo &&
            <div>
                {props.adinfo.hasOwnProperty('error') &&
                    <div>
                        <div className={classes.close}><Icon icon={closeOutline} height={20} width={20} color={'red'}/> </div>
                        <div className={classes.error_title}>{props.adinfo['error']}</div>
                        <div className={classes.error_info}>Попробуйте открыть другое объявление или перезагрузить программу.</div>
                    </div>
                }
                {!props.adinfo.hasOwnProperty('error') &&
                    <div>
                        <div className={classes.header}>{title}</div>
                        <div className={classes.scroll_cont}>
                            <div className={classes.img_big}>
                                <p style={{margin:0}}><img src={bigImg['1280x960']} style={{maxWidth:480}} height='360'/></p>
                            </div>
                            <div className={classes.img_cont} style={{overflowY: 'auto', marginLeft:16, height: 360}}>
                                {img.map((image) => 
                                <div className={classes.img_item} onClick={() => setImg(image)}>
                                    <img src={image['140x105']} height='109.33' width='145,77' className={classes.img_image}/>
                                </div>
                                )}
                            </div>
                            <div>
                                <div className={classes.price}>Цена: {price['value_signed']}</div>
                                <div className={classes.date}>{date}</div>
                            </div>
                            <div className={classes.address}>{address}</div>
                            <div className={classes.data_header}>Описание:</div>
                            <div className={classes.desc}>
                                {desc}
                            </div>
                            <div className={classes.data_header}>Характеристики:</div>
                            <div className={classes.params}>
                                
                                <Grid container direction="row" >
                                    {params.map((param) => 
                                    <Grid sm={12} md={5}  item className={classes.param_item}>
                                        {param['title']}: {param['description']}
                                    </Grid>)}
                                </Grid>
                            </div>
                        </div>
                        <Button className={classes.btn} onClick={() =>{window.open(url, '_blank', 'location=yes,height=600,width=800,scrollbars=yes,status=yes');}}>Подробнее</Button>
                    </div>
                }
            </div>
        }
        
        {!props.adinfo &&
            <div>
                <div className={classes.desc}>gggggggggggggggggggggggggs</div>
            </div>
        }
    </Grid>;
    }
    
    
    let mapStateToProps = (state) => {
    return {
        adinfo: state.adinfo,
    }
    }
    
    
    const ComponetConnect = connect(mapStateToProps)(Componet);

export default ComponetConnect;

