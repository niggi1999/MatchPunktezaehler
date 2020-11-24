import React from 'react';
import axios from 'axios';
import Procedure from './procedure';
import "./App.css"

class App extends React.Component {
constructor(){
    super()
      this.state = {
        data: {status: 'game',
          connectedController: 1,
          activeChooseField: 1,
          playMode: 1, activeChooseField1: 5, activeChooseField2: null,
          playMode: 1, activeChooseField1: 8, activeChooseField2: null,
          activeChooseField: 0,
          counterTeam1: 11, counterTeam2: 12, roundsTeam1: 2, roundsTeam2: 1, gamesTeam1:7, gamesTeam2: 6,
          team1HighColor: 'Green', team1DownColor: 'Orange', team2HighColor: 'Blue', team2DownColor: 'Red', team1Left: 1,
          opacityHighSiteTeam1: 0.5, opacityDownSiteTeam1: 0.5, opacityHighSiteTeam2: 0.5, opacityDownSiteTeam2: 0.5}
      }

    this.eventSource = new EventSource("http://localhost:5000/events");
    this.updateState = this.updateData.bind(this)

  }
  
  componentDidMount() {

      this.eventSource.addEventListener('updateData', e =>
      this.updateData(JSON.parse(e.data))
    );

  axios.get("http://localhost:5000/",
  {headers: {'Access-Control-Allow-Origin': '*'}
  })
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            data: result.data
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }
 
    updateData(newState) {
      console.log("Server side event recieved at",new Date())
      this.setState(Object.assign({}, { data: newState }));
  }
    
  render() {
    return (
      <div className="app">
        <Procedure data={this.state.data}/>
      </div>
    )
}
}
export default App;
