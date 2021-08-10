import '../css/App.css';
import Menu from './Menu/Menu';
import Main from './Main/Main';
import React, { Component } from "react";
import "../css/App.css";
import {eel} from './eel';



class App extends Component {
  constructor(props) {
    super(props);
    eel.set_host("ws://localhost:8888");

    this.state = {
    parsers: null,
    settings: null,

    };
  }

  render() {
    
    return (
      <div className="App">
        <Menu />
        <Main parsers={this.state.parsers}/>
      </div>
    );
  }
}

export default App;
