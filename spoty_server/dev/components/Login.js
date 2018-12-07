import React, { Component } from 'react';

class Login extends Component {

  constructor(props){
    super(props);
    this.state = {
      url : "",
      loaded : false
    };
  }

  componentDidMount(){
    fetch("/get_login_url")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({url : result.url, loaded : true});
        },
        (error) => {
          alert("error -> "+error); // DEBUG
        }
      )
  }

  render(){
    if (this.state.loaded){
      return(
        <div className="jumbotron">
          <h3>Jarraitzeko logeatu mesedez:</h3>
          <p><a className="btn btn-primary btn-lg" href={this.state.url} role="button">Klikatu Hemen</a></p>
        </div>
      );
    }else{
      return(<h3>Loading...</h3>)
    }
  }
}

export default Login;
