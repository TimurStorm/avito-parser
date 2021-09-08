import { Grid, ThemeProvider, TextField, Checkbox, Typography, Accordion, AccordionSummary, AccordionDetails} from '@material-ui/core';
import { makeStyles , createTheme, withStyles} from '@material-ui/core/styles';
import '../../../css/Scroll.css';
import Ad from './Ad';
import React, {useState} from 'react';
import {connect} from 'react-redux';
import searchOutline from '@iconify-icons/eva/search-outline';

var ads_height = 450;

const AdInfo = makeStyles({
    main: {
        height: 623,
        minWidth: 252,
        padding: '24px 16px',
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
        minWidth:170,
    },
    filts:{
        float:'left'
    },
    label: {
        fontSize: 13,
        fontWeight: 300,
    },
    ads: {
        minWidth: 220,
        marginTop: 12,
        height: ads_height,
        overflowY: 'auto',
    },
    textField: {
        width: 220,
        '&:before': {
            borderColor: '#26A18D',
        },
        '&:after': {
            borderColor: '#26A18D',
        },
    },
    accord_cont:{
        background: '#0d1c1f',
        border: '1 solid',
        color: '#dfdfdf',
    },
    accord_item_text:{
        float:'left',
        marginTop:12,
    },
    accord_item_check:{
        float:'left',
    },
    accord_button:{
        background: '#26A18D',
        color: '#dfdfdf',
    }
});

const GreenCheckbox = withStyles({
    root: {
    float: 'right',
    color: '#26A18D',
    '&$checked': {
        color: '#26A18D',
    },
    },
    checked: {},
  })((props) => <Checkbox color="default" {...props} />);

const theme = createTheme({
    typography: {
      fontFamily: 'sans-serif',
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

function Componet(props) {

    var check = [];
    if (props.parsers.length > 0)
    console.log(props.parsers.length);
    for (let i=0;i< props.parsers.length; i++){
        check.push(true)
    }
    console.log(check);
    const classes = AdInfo(props);
    
    const [accordOpen, setAccordOpen] = useState(false);
    const [search, setSearch] = useState('');
    const [checkParsers, setCheckParsers] = useState(check);
    const handleClick = (event) => {
        setAccordOpen(event.currentTarget);
    };
    console.log(checkParsers)
    const handleAccardi = () => {
        if (accordOpen == false){
            while (ads_height > 220){
                ads_height -= 1;
            }
            setAccordOpen(true);
        } 
        else{
            setTimeout(() => {
                while (ads_height < 450){
                    ads_height += 0.5;
                }
                setAccordOpen(false);
            }, 200);
            
        }
    }


    const filteredData = props.data.filter( elem => {
        return elem[0].toLowerCase().includes(search.toLowerCase());
    });

    const setCheck = (id) => {
        let x = checkParsers;
        console.log(checkParsers);
        if (x[id] == true){
            x[id] = false;
        }
        else{
            x[id] = true;
        }
        setCheckParsers(x);
        
    }

    const ads = filteredData.map((ad)=> <Ad 
        title={ad[0]} 
        price={ad[1]}
        parser={ad[2]}
        url={ad[3]} />);
    return <Grid  item  md={2} lg={2} sm={2} xs={2} className={classes.main}>
        <div className={classes.header}>Объявления</div>
        <div className={classes.filter}>
            <ThemeProvider theme={theme}>
                <div className={classes.filts}>
                    <TextField
                        icon={searchOutline}
                        placeholder='Поиск'
                        InputProps={{
                            className: classes.textField
                        }}
                        onChange={(event) => setSearch(event.target.value)}
                    />
                </div>
            </ThemeProvider>
        </div>
        <Accordion TransitionProps={{className: classes.accord_cont}} >
            <AccordionSummary onClick={() => {handleAccardi()}} className={classes.accord_button}>
                <Typography>Поиски</Typography>
            </AccordionSummary>
            <AccordionDetails>
                <ThemeProvider theme={theme}>
                    {props.parsers.length > 0 &&
                    <div style={{width: 220}}>
                        {props.parsers.map((parser) => 
                        <div onClick={handleClick} style={{height: 44}} onClick={() => {setCheck(props.parsers.indexOf(parser))}}>
                            <div className={classes.accord_item_text}>
                                {parser['title'].length >= 15 && 
                                    <a>{parser['title'].slice(0,14) + '...'}</a>
                                }
                                {parser['title'].length < 15 && 
                                    <a>{parser['title']}</a>
                                }
                            </div>
                            <GreenCheckbox classNames={classes.accord_item_check}/>
                        </div>)}
                    </div>
                    }
                    {props.parsers.length == 0 &&
                    <div>
                        Нет парсеров
                    </div>
                    }
                </ThemeProvider>  
            </AccordionDetails>
        </Accordion>
             
        

        
        
        <div className={classes.ads} style={{height: ads_height}}>
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



const ComponetConnect = connect(mapStateToProps)(Componet);

export default ComponetConnect;