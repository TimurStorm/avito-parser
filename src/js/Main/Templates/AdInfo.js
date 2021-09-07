import { Grid, ThemeProvider, TextField, Checkbox} from '@material-ui/core';
import { makeStyles , createTheme, withStyles} from '@material-ui/core/styles';
import '../../../css/Scroll.css';
import {Button, Menu, MenuItem} from '@material-ui/core';
import Ad from './Ad';
import React, {useState} from 'react';
import {connect} from 'react-redux';
import searchOutline from '@iconify-icons/eva/search-outline';

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
        height:450,
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
    parsers_button:{
        textTransform: 'none',
        border: '1px solid',
        borderRadius: 5,
        borderColor: '#26A18D',
        paddingLeft: 66,
        paddingRight: 66,
        width: 220,
        marginTop: 8,
        '&:hover': {
          backgroundColor: '#239481',
        },
    },
    parsers_menu:{
        backgroundColor: '#102326',
    },
    parsers_menu_items:{
        backgroundColor: '#102326',
        color: '#dfdfdf',
        width: 220,
        '&:hover': {
            backgroundColor: '#102326',
          },
    },

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
    
    const [anchorEl, setAnchorEl] = useState(null);

    const handleClick = (event) => {
      setAnchorEl(event.currentTarget);
    };
  
    const handleClose = () => {
      setAnchorEl(null);
    };

    const classes = AdInfo(props);
    const [search, setSearch] = useState('');

    const filteredData = props.data.filter( elem => {
        return elem[0].toLowerCase().includes(search.toLowerCase());
    });

    const ads = filteredData.map((ad)=> <Ad 
        title={ad[0]} 
        price={ad[1]}
        parser={ad[2]}
        url={ad[3]} />);
    // TODO: ПОРЕШАТЬ ДАТУ НА ОБЪЕКТЫ ЧТОБЫ БЫЛИ ОБЪЯВЛЕНИЯ 
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

        <Button aria-controls="simple-menu" aria-haspopup="true" className={classes.parsers_button} onClick={handleClick}>
        Парсеры
        </Button>
        <Menu
            id="simple-menu"
            anchorEl={anchorEl}
            MenuListProps={{className:classes.parsers_menu}}
            keepMounted
            open={Boolean(anchorEl)}
            onClose={handleClose}
        >
        <ThemeProvider theme={theme}>
        {props.parsers.length == 2 &&
        <div>
             {props.parsers.map((parser) => 
             <MenuItem onClick={handleClick} className={classes.parsers_menu_items}>
                 <div>{parser['title']}</div>
                 <div><GreenCheckbox /></div>
            </MenuItem>)}
        </div>
        }
        {props.parsers.length != 2 &&
        <div>
            Нет парсеров
        </div>
        }
        </ThemeProvider>       
        </Menu>

        
        
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



const ComponetConnect = connect(mapStateToProps)(Componet);

export default ComponetConnect;