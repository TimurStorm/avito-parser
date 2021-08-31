import '../../css/Menu.css';
import MenuButton from './Buttons/MenuButtons';
import React from 'react';

import {Grid} from "@material-ui/core";

import CreateParser from './Buttons/СreateParser';
import homeOutline from '@iconify-icons/eva/home-outline';
import starOutline from '@iconify-icons/eva/star-outline';
import settings2Outline from '@iconify-icons/eva/settings-2-outline';
import personOutline from '@iconify-icons/eva/person-outline'
import {connect} from 'react-redux';


function Componet(props){

  let titles = ['Избранное', 'Настройки', 'Профиль'];
  let icons = [starOutline, settings2Outline, personOutline];
  let hrefs = props.hrefs;

  let low_buttons = titles.map((title, id=titles.indexOf(title)) => <MenuButton 
  title={title} 
  href = {hrefs[id]}
  icon={icons[id]} />);
  
  return <Grid  item  md={2} lg={2} sm={2} xs={2} className="Menu">
        <MenuButton title='Главная' icon={homeOutline} href='.'/>
        <CreateParser />
        {low_buttons}
    </Grid>
  
}

let mapStateToProps = (state) => {
  return {
      hrefs: state.hrefs,
  }
}

let MenuConnect = connect(mapStateToProps)(Componet)

export default MenuConnect;