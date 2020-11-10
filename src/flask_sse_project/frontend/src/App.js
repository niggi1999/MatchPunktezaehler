import React from 'react';
import axios from 'axios';
import Procedure from './procedure';
import "./App.css"

class App extends React.Component {
constructor(){
    super()
      this.state = {
        data: [
          {status: 'game'}, //data for Procedure
          {connectedController: 1}, //data for Init
          {activeChooseField: 1}, //data for Player-Menu
          {playMode: 1, activeChooseField1: 5, activeChooseField2: null}, //data for Name Selection Team 1
          {playMode: 1, activeChooseField1: 8, activeChooseField2: null}, //data for Name Selection Team 1
          {activeChooseField: 0} // data for Game-Menu
        ]

      };
    this.eventSource = new EventSource("http://localhost:5000/events");
    this.updateState = this.updateState.bind(this)

  }
  
  componentDidMount() {

      this.eventSource.addEventListener("updateData", e =>
      this.updateState(JSON.parse(e.data))
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
     updateState(newState) {
        console.log("Server side event recieved at",new Date())
        this.setState(Object.assign({}, { data: newState }));
      }

       
    
  render() {
    return (
      <div className="app">
        <h1>Test: {this.state.data.counterTeam1}</h1>
        <Procedure data={this.state.data}/>
      </div>
    )
}
}
export default App;
