import React from 'react';
import Backdrop from '@material-ui/core/Backdrop';
import MenuButton from './MenuButtons';
import { makeStyles, createTheme, ThemeProvider} from '@material-ui/core/styles';
import personOutline from '@iconify-icons/eva/person-outline';
import closeOutline  from '@iconify-icons/eva/close-outline';
import { Icon} from '@iconify/react';

const Profile = makeStyles((theme) => ({
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
  },
  main: {
    height: 400,
    width: 300,
    backgroundColor: '#102326',
    padding: 24,
    border: '0 solid',
    borderRadius: 5,
    color: '#dfdfdf',
  },
  title: {
    fontSize: 20,
    fontWeight: 500,
    float: 'left',
  },
  avatar_cont:{
    marginTop: 16,
    width: '100%',
    padding: '0px 75px'
  },
  avatar_img:{
    height:150,
    width:150,
    border: '0 solid',
    borderRadius: 100,
    background:'#239481'
  },
  close:{
    float: 'right',
    cursor: 'pointer',
  },
  info_cont:{
    textAlign: 'center',
    marginTop:16,
  },
  info_item:{
    marginBottom:8,
  }
}));

export default function StyledComponents() {
  const classes = Profile();
  const [open, setOpen] = React.useState(false);

  

  const handleClose = () => {
    setOpen(false);
  };
  const handleToggle = () => {
    setOpen(!open);
  };


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
      <MenuButton title={'Профиль'} click={handleToggle} icon={personOutline}>

      </MenuButton>
      <Backdrop className={classes.backdrop} open={open}>
        <ThemeProvider theme={theme}>
          <div className={classes.main}>
            <div>
                <div className={classes.close} onClick={handleClose}><Icon icon={closeOutline} height={20} width={20} color={'red'}/> </div>
            </div>
            <div className={classes.avatar_cont}>
                <a><div className={classes.avatar_img}></div></a>
            </div>
            <div className={classes.info_cont}>
                <div className={classes.info_item} style={{fontSize: 18, fontWeight: 200}}>Тимур Мазитов</div>
                <div className={classes.info_item} style={{fontSize: 12, fontWeight: 300}}>noobofmylive@gmail.com</div>
                <div className={classes.info_item} style={{color:'#1b6259'}}>БЕТА: в дальнейшем тут будет дополнительное описание пользователя</div>
            </div>
          </div>
        </ThemeProvider>
      </Backdrop>
    </div>
  );
}