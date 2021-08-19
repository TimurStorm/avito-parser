import '../../css/Menu.css';
import MenuButton from './Buttons/MenuButtons';
import {useEffect} from 'react';
import React from 'react';
import {async_eel_get_all_parsers} from '../Async/asyncActions.js';

import {Grid} from "@material-ui/core";

import CreateParser from './Buttons/СreateParser';
import homeOutline from '@iconify-icons/eva/home-outline';
import starOutline from '@iconify-icons/eva/star-outline';
import settings2Outline from '@iconify-icons/eva/settings-2-outline';
import personOutline from '@iconify-icons/eva/person-outline'
import bookOutline from '@iconify-icons/eva/book-outline';
import {connect} from 'react-redux';


function Componet(props){

  useEffect(() => {
    props.getParsers();
  },[]);

  let titles = ['Избранное', 'Настройки', 'Профиль'];
  let icons = [starOutline, settings2Outline, personOutline];
  let hrefs = props.hrefs;
  let parsers = props.parsers; 

  let low_buttons = titles.map((title, id=titles.indexOf(title)) => <MenuButton 
  title={title} 
  href = {hrefs[id]}
  icon={icons[id]} />);

  let pars_buttons;
  if (parsers[0]){
    pars_buttons = parsers[0].map((title, id=titles.indexOf(title)) => <MenuButton 
    title={title} 
    href = {'/parser/'+id}
    icon={bookOutline} />);
  }
  
  return <Grid  item  md={2} lg={2} sm={2} xs={2} className="Menu">
        <MenuButton title='Главная' icon={homeOutline} href='.'/>
        <CreateParser />
        <hr color={'#17554d'} style={{marginTop:0 , marginBottom: 17}} size={2}/>
        <div className='Parsers'>
          {pars_buttons}
        </div>
        <hr color={'#17554d'} style={{marginTop:0 , marginBottom: 17}} size={2}/>
        {low_buttons}
    </Grid>
  
}

let mapStateToProps = (state) => {
  return {
      hrefs: state.hrefs,
      parsers: state.parsers
  }
}

let mapDispatchToProps = (dispatch) => {
  return {
      getParsers: () => {
          dispatch(async_eel_get_all_parsers());
      }
  }
}

let MenuConnect = connect(mapStateToProps, mapDispatchToProps)(Componet)

export default MenuConnect;