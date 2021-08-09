import Ads from './Templates/MainBlock';
import React, { Component } from 'react';
import '../../css/Main.css';
import {eel} from '../eel';

class Main extends Component {
  constructor(props) {
    super(props);
    this.state = { ads: [] };
  }

  async componentDidMount(){
    
  }
  //<SupportOne/>
  render() {
    return <div className='Main'>
        <Ads/>
    </div>
  }
}

export default Main;