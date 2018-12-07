import React, { Component } from 'react';

class PlaylistSelect extends Component {

  constructor(props){
    super(props);
    this.state = {
      playlists : [],
      loaded : false
    };

    this.listPlaylists = this.listPlaylists.bind(this);
  }

  componentDidMount(){
    fetch("/get_playlists", {
      headers : {
        "Accept" : "application/json",
        "Content-Type" : "application/json"
      },
      method : 'POST',
      body : JSON.stringify({"username" : "oierlas"})
    })
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({loaded : true, playlists: result.playlists})
        },
        (error) => {
          alert("error -> "+error); // DEBUG
        }
      )
  }

  listPlaylists(pl, i){
    return(<p key={i}>{pl.name} {pl.id}</p>);
  }

  render(){
    if (this.state.loaded){
      return(
        <div className="panel panel-default">
          <div className="panel-body">
            <h4> Aukeratu playlistak: </h4>
            {
              this.state.playlists.map(this.listPlaylists)
            }
            <button className="btn btn-info">Ados!</button>
          </div>
        </div>
      );
    }else{
      return(<h3>Loading...</h3>);
    }
  }
}

export default PlaylistSelect;
