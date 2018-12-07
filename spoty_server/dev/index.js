import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import './css/index.css';
import App from './App';
import {CookiesProvider} from 'react-cookie';

class Index extends Component {
  render(){
    return(
      <CookiesProvider>
        <App/>
      </CookiesProvider>
    );
  }
}

ReactDOM.render(<Index />, document.getElementById('root'));
