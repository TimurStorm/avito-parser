import { makeStyles} from '@material-ui/core/styles';
import React from 'react';

const SupportOne = makeStyles({
    main: {
        height: 71,
        width: 122,
        padding: 23,
        backgroundColor: '#102326',
        marginRight: 16,
        border: '0 solid',
        borderRadius: 5,
    }
});

function Component(props){
    const classes = SupportOne(props);

    return <div className={classes.main}>

    </div>
}

export default Component;