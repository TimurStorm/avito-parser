import '../css/App.css';
import Menu from './Menu/Menu';
import Ads from './Main/Templates/MainBlock';
import AdInfo from './Main/Templates/AdInfo'; 
import React, { Component } from "react";
import "../css/App.css";
import Grid from '@material-ui/core/Grid';
import {connect} from 'react-redux';
import {async_eel_get_all_parsers, async_eel_get_parser_ads} from './Async/asyncActions';
import {eel} from './heel';

eel.set_host("http://localhost:8000");

class App extends Component {
  constructor(props) {
    super(props);    
    console.log(window);
    eel.expose(props.getAds, 'set_js_ads');
    eel.expose(props.getParsers, 'set_js_parser');
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

let mapDispatchToProps = (dispatch) => {
  return {
      getParsers: () => {
          dispatch(async_eel_get_all_parsers());
      },
      getAds: () => {
          dispatch(async_eel_get_parser_ads());
      }
  }
}

const ComponetConnect = connect(null, mapDispatchToProps)(App);

export default ComponetConnect;
