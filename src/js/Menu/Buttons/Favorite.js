import React from 'react';
import Backdrop from '@material-ui/core/Backdrop';
import MenuButton from './MenuButtons';
import { makeStyles, createTheme, ThemeProvider} from '@material-ui/core/styles';
import starOutline from '@iconify-icons/eva/star-outline';

const Profile = makeStyles((theme) => ({
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
  },
  main: {
    height: 300,
    width: 400,
    backgroundColor: '#102326',
    padding: 24,
    border: '0 solid',
    borderRadius: 5,
    color: '#dfdfdf',
  },
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
      <MenuButton title={'Избранное'} click={handleToggle} icon={starOutline}>

      </MenuButton>
      <Backdrop className={classes.backdrop} open={open} onClick={handleClose}>
        <ThemeProvider theme={theme}>
          <div className={classes.main}>

            
          </div>
        </ThemeProvider>
      </Backdrop>
    </div>
  );
}