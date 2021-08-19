import { makeStyles} from '@material-ui/core/styles';
import React from 'react';

const SupporTwo = makeStyles({
    main: {
        height: 97,
        width: 570,
        padding: 10,
        backgroundColor: '#102326',
        border: '0 solid',
        borderRadius: 5,
    }
});

function Component(props){
    const classes = SupporTwo(props);

    return <div className={classes.main}>

    </div>
}

export default Component;