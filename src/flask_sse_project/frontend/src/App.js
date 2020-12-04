import React from 'react';
import axios from 'axios';
import Procedure from './procedure';
import "./App.css"

class App extends React.Component {
constructor(){
    super()
      this.state = {
        data: {status: 'playerMenu', //always needed
          cursorElement: "Badminton", //always needed

          connectedController: 1, //for initSite
          
          activeChooseField: "1vs1", //for PlayerMenuSite

          //fieldNames: ["1vs1", "2vs2"], //for PlayerMenuSite

          playMode: 1, color1Team1: "Green", color2Team1: null, //for nameMenuSite
          color1Team2: "Red", color2Team2: null, //for nameMenuSite
          fieldNames: ["Orange", "Red", "Purple", "Blue", "Green", "Black"], //for nameMenuSite
          tableActive: 1,

          activeChooseField: "Badminton", //for GameMenuSite
          fieldNames: ["Badminton", "Volleyball", "Tennis"], //for GameMenuSite

          counterTeam1: 11, counterTeam2: 12, roundsTeam1: 1, roundsTeam2: 1, gamesTeam1:7, gamesTeam2: 6, //for GameSite
          team1HighColor: 'Green', team1DownColor: 'Orange', team2HighColor: 'Blue', team2DownColor: 'Red', team1Left: false, //for GameSite
          opacityHighSiteTeam1: 0.2, opacityDownSiteTeam1: 1, opacityHighSiteTeam2: 0.2, opacityDownSiteTeam2: 0.2, //for GameSite

          team: 1, // for changeSide
      }
          
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
