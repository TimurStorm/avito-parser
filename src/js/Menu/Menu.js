import '../../css/Menu.css';
import MenuButton from './Buttons/MenuButtons';
import React from 'react';

import {Grid} from "@material-ui/core";

import CreateParser from './Buttons/CreateFinder';
import Favorite from './Buttons/Favorite';
import Profile  from './Buttons/Profile';
import Settings from './Buttons/Settings';

import homeOutline from '@iconify-icons/eva/home-outline';


function Menu(props){
  return <Grid  item  md={2} lg={2} sm={2} xs={2} className="Menu">
        <MenuButton title='Главная' icon={homeOutline} href='.'/>
        <CreateParser />
        <Favorite/>
        <Profile/>
        <Settings/>
    </Grid>
  
}


export default Menu;