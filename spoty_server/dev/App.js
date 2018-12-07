import React, { Component } from 'react';
import { instanceOf } from 'prop-types';
import { withCookies, Cookies } from 'react-cookie';
import Login from './components/Login.js';
import PlaylistSelect from './components/PlaylistSelect.js';
import './css/App.css';

class App extends Component {
  static propTypes = {
    cookies : instanceOf(Cookies).isRequired
  }

  constructor(props){
    super(props);

    const {cookies} = props;

    this.state = {
      token : cookies.get("authtoken") || false
    };
  }

  render() {
    if (this.state.token){
      return (
        <div className="App">
          <PlaylistSelect/>
        </div>
      );
    }else{
      return (
        <div className="App">
          <Login/>
        </div>
      );
    }
  }
}

export default withCookies(App);
