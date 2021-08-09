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

  async componentDidMount(){
    console.log(1);
    //await eel.start_all_parsers()();
    console.log(1);
    var all_parsers = await eel.get_all_parsers()();
    console.log(1);
    var all_settings = await eel.get_all_settings()();
    console.log(1);
    console.log(all_parsers);
    console.log(all_settings);
    this.setState({
        settings: all_settings,
        parsers: all_parsers,
    });
  }

  render() {
    
    return (
      <div className="App">
        <Menu />
        <Main />
      </div>
    );
  }
}

export default App;
