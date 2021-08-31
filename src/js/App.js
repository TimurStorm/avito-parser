import '../css/App.css';
import Menu from './Menu/Menu';
import Ads from './Main/Templates/MainBlock';
import AdInfo from './Main/Templates/AdInfo'; 
import SupportOne from './Main/Templates/Support-1';
import SupportTwo from './Main/Templates/Support-2';
import React, { Component } from "react";
import "../css/App.css";
import {eel} from './eel';
import Grid from '@material-ui/core/Grid';



class App extends Component {
  constructor(props) {
    super(props);
    eel.set_host("ws://localhost:8888");
  }
  async componentDidMount(){
    await eel.start_all_parsers()();
  }

  render() {
    
    return (
      
      <div className="App">
        <Grid container
          direction="row"
          wrap='nowrap'
          >
           <Menu/>
           <Ads/>
           <AdInfo/>
          </Grid>
        
        
      </div>
    );
  }
}

export default App;
