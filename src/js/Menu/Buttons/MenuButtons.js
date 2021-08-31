import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import { Icon} from '@iconify/react';
import React from 'react';

const MenuButton = makeStyles({
    colors:{
      'main_color': '#223639',
      'font_color': '#dfdfdf',  
    },
    
    main: {
        
        marginBottom: 25,
        height: 30,
        width: '100%',
        minWidth: 200,
        fontFamily: 'Rubik',
        fontWeight: 'regular',
        padding: 0,
        textTransform: 'none',
        '&:hover': {
            background: '#2d474b',
        },
        
        
    },
    sign: {
        width: '6px',
        height: 30,
        marginRight: 5,
        border: '0 solid',
        borderRadius: '5px 0 0 5px',
    },
    label: {
        color: '#dfdfdf',
        align: "left",
        width: 200,
        textAlign: 'left',
        fontSize: '15px',
        padding: 4,
        margin: 0,
    },
    icon: {
        color: '#dfdfdf',
        height: 20,
        width: 20,
        paddingRight: 7,
    },
    
});
  
export default function StyledComponents(props) {
    const classes = MenuButton();
    let title = props.title;
    let icon = props.icon;
    let href = props.href;
    let click = props.click;
    return <Button className={classes.main} href={href} onClick={click}>
        <div className={classes.sign}></div>
        <div className={classes.label}>
            {title}
        </div>
        <div className={classes.icon}>
            <Icon icon={icon} height={20} width={20} />    
        </div>
          
    </Button>;
}