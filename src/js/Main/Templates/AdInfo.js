import { Grid, ThemeProvider, TextField} from '@material-ui/core';
import { makeStyles , createTheme} from '@material-ui/core/styles';
import '../../../css/Scroll.css';
import Ad from './Ad';
import React, {useEffect} from 'react';
import searchOutline from '@iconify-icons/eva/search-outline';
import {connect} from 'react-redux';
import {async_eel_get_all_parsers, async_eel_get_parser_ads} from '../../Async/asyncActions';

const AdInfo = makeStyles({
    main: {
        height: 623,
        width:"30%",
        padding: '24px 15px',
        backgroundColor: '#102326',
        border: '0 solid',
        borderRadius: 5,
        color: '#dfdfdf',
        marginRight:16,
        marginTop: 32,
    },
    header:{
        width:'100%',
        fontSize: 20,
        fontWeight: 500,
        float:'left'
    },
    filter:{
        margin: '5px 0px 5px 0px',
        display: 'inline-block',
        width:'100%',
        minWidth:83,
    },
    filts:{
        float:'left'
    },
    label: {
        fontSize: 13,
        fontWeight: 300,
    },
    ads: {
        marginTop: 12,
        height:505,
        overflowY: 'auto',
        width:'100%',
        minWidth:83,
    },
    textField: {
        '&:before': {
            borderColor: '#26A18D',
        },
        '&:after': {
            borderColor: '#26A18D',
        },
    },
    
});

const theme = createTheme({
    typography: {
      fontFamily: 'Rubik',
      fontSize: 14,
      fontWeight: 'light',
    },
    palette: {
      primary: {
        main: '#26A18D',
      },
      text: {
        primary: '#dfdfdf',
        secondary: '#26A18D',
        disabled: '#dfdfdf',
        hint: '#dfdfdf',
      },
      divider: '#26A18D',
    },
  });
/**
 *  FROM RETURN
 * <div className={classes.filts} style={{marginLeft:215}} >
                
                    <FormControlLabel
                    InputProps={{'classes': classes.chek}}
                    value="start"
                    control={<Checkbox color="primary" />}
                    label="Только новые"
                    labelPlacement="start"
                    />
                
            </div>
            <div className={classes.filts}>
                <Select
                style={{marginLeft: 40}}
                value='По умолчанию'
                >
                    <MenuItem value={'По умолчанию'}>По умолчанию</MenuItem>
                    <MenuItem value={'Сначала дорогие'}>Сначала дорогие</MenuItem>
                    <MenuItem value={'Сначала дешёвые'}>Сначала дешёвые</MenuItem>
                </Select>

            </div>
 */
function Componet(props) {
    
    const classes = AdInfo(props);

    useEffect(() => {
        props.getParsers();
        props.getAds();
        setInterval(() => { props.getAds()}, 1500);
    },[])
    const ads = props.data.map((ad)=> <Ad 
        title={ad[0]} 
        price={ad[1]}
        parser={ad[2]}
        url={ad[3]} />);
    // TODO: ПОРЕШАТЬ ДАТУ НА ОБЪЕКТЫ ЧТОБЫ БЫЛИ ОБЪЯВЛЕНИЯ 
    return <Grid  item  md={2} lg={2} sm={2} xs={3} className={classes.main}>
        {document.documentElement.clientWidth >= 880 &&
            <div className={classes.header}>Объявления</div>
        }
        {document.documentElement.clientWidth < 880 &&
            <div className={classes.header}>Объяв.</div>
        }
        <div className={classes.filter}>
            <ThemeProvider theme={theme}>
            <div className={classes.filts}>
                <TextField
                    icon={searchOutline}
                    placeholder='Поиск'
                    InputProps={{
                        className: classes.textField
                    }}
                    />
                </div>
            
            </ThemeProvider>
        </div>
        
        <div className={classes.ads}>
            {ads}
        </div>
    </Grid>  
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