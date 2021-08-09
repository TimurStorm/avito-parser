import '../../css/Menu.css';
import MenuButton from './Buttons/MenuButtons';
import {Component} from 'react';
import React from 'react';
import CreateParser from './Buttons/СreateParser';
import homeOutline from '@iconify-icons/eva/home-outline';
import starOutline from '@iconify-icons/eva/star-outline';
import settings2Outline from '@iconify-icons/eva/settings-2-outline';
import personOutline from '@iconify-icons/eva/person-outline'


class Menu extends Component {
  constructor(props) {
    super(props);
    this.state = {
      titles : ['Главная', 'Избранное', 'Настройки', 'Профиль'],
      icons : [homeOutline,  starOutline, settings2Outline, personOutline],
      hrefs : ['.', '/favorite', '/settings','/profile']
    };
  }

  render() {
    let buttons = this.state.titles.map((title, id=this.state.titles.indexOf(title)) => <MenuButton 
    title={title} 
    id={id}
    href = {this.state.hrefs[id]}
    icon={this.state.icons[id]} />)
    return (
      <div className="Menu">
          {buttons}
          <CreateParser />
      </div>
    );
  }
}

export default Menu;