import React from 'react';
import Backdrop from '@material-ui/core/Backdrop';
import MenuButton from './MenuButtons';
import plusCircleOutline from '@iconify-icons/eva/plus-circle-outline';
import { makeStyles, createTheme, ThemeProvider } from '@material-ui/core/styles';
import { Icon} from '@iconify/react';
import closeOutline  from '@iconify-icons/eva/close-outline';
import TextField from '@material-ui/core/TextField';
import Slider from '@material-ui/core/Slider';
import Button from '@material-ui/core/Button';
import {eel} from '../../eel';

const CreateParser = makeStyles((theme) => ({
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
  },
  main: {
    height: 300,
    width: 400,
    backgroundColor: '#102326',
    padding: '15px 25px',
    border: '0 solid',
    borderRadius: 5,
    color: '#dfdfdf',
  },
  title: {
    fontSize: 20,
    fontWeight: 500,
    float: 'left',
  },
  label: {
    fontFamily: 'Rubik',
    fontSize: 12,
    fontWeight: 400,
    color: '#26A18D',
    paddingBottom: 15,
  },
  timer: {
    width: 190
  },
  items: {
    paddingTop: 30,
  },
  item: {
    marginTop: 19,
  },
  textField: {
    '&:before': {
      borderColor: '#26A18D',
    },
    '&:after': {
      borderColor: '#26A18D',
    },
  },
  close:{
    float: 'right',
    cursor: 'pointer',
  },
  create: {
    
    marginRight: 0,
    textTransform: 'none',
    backgroundColor: '#26A18D',
    paddingRight: 66,
    paddingLeft: 66,
    '&:hover': {
      backgroundColor: '#239481',
    },
  }
}));

export default function StyledComponents() {
  const classes = CreateParser();
  const [open, setOpen] = React.useState(false);
  const [title, setTitle] = React.useState('');
  const [url, setUrl] = React.useState('');
  const [timer, setTimer] = React.useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    let responce = await eel.create_parser(title, url, timer)();
    if (responce){
      handleClose();
    }
    else {
      //TODO: переделать в всплывающее уведомление
      console.log('Ошибка создания парсера');
    }
  }

  const handleClose = () => {
    setOpen(false);
  };
  const handleToggle = () => {
    setOpen(!open);
  };

  const marks =[
    {
      value: 1,
      label: '1'
    },
    {
      value: 15,
      label: '15'
    },
    {
      value: 30,
      label: '30'
    },
    {
      value: 45,
      label: '45'
    },
    {
      value: 60,
      label: '60'
    }
  ]

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
  //
  return (
    <div>
      <MenuButton title={'Создать парсер'} click={handleToggle} icon={plusCircleOutline}>

      </MenuButton>
      <Backdrop className={classes.backdrop} open={open}>
        <ThemeProvider theme={theme}>
          <div className={classes.main}>

            <div className={classes.title}>Новый парсер</div>
            <div className={classes.close} onClick={handleClose}><Icon icon={closeOutline} height={20} width={20} color={'red'}/> </div>
            <div className={classes.items}>
              <form noValidate autoComplete='off' onSubmit={handleSubmit}>
              <div className={classes.item}>
                <TextField 
                  label='Название'
                  onChange={(e) => setTitle(e.target.value)}
                  InputLabelProps={{
                    shrink: true,
                  }}
                  InputProps={{
                    className: classes.textField
                  }}
                  />
              </div>
              <div className={classes.item}>
                <TextField 
                  label='Ссылка'
                  onChange={(e) => setUrl(e.target.value)}
                  InputLabelProps={{
                    shrink: true,
                  }}
                  InputProps={{
                    className: classes.textField
                  }}
                  />
              </div>
              <div className={classes.item}>
                  <div className={classes.label}>
                    Таймер
                  </div>
                  <Slider
                  aria-label='Таймер'
                  className={classes.timer}
                  onChange={(e, val) => setTimer(val)}
                  step={1}
                  min={1}
                  max={60}
                  valueLabelDisplay="auto"
                  marks={marks}
                  />
              </div>
              <Button 
              className={classes.create} 
              type='submit'
              >
                Cоздать
              </Button>
              </form>
            </div>
          </div>
        </ThemeProvider>
      </Backdrop>
    </div>
  );
}