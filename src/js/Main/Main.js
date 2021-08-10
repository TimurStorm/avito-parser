import Ads from './Templates/MainBlock';
import React, { Component } from 'react';
import '../../css/Main.css';
import {eel} from '../eel';

class Main extends Component {
  constructor(props) {
    super(props);
    this.state = { parsers: props.parsers };
  }
  
  render() {
    return <div className='Main'>
        <Ads ads={this.state.ads}/>
    </div>
  }
}

export default Main;