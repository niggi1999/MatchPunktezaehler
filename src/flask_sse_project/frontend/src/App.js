import React from 'react';
import './App.css';
import axios from 'axios';
import Teamview from './teamview';
import Counter from './counter';

class App extends React.Component {
constructor(){
    super()
      this.state = {
        data: [],
        leftSideTeam: '',
        rightSideTeam: 'hALLO',
        leftSideFirstContact: 0,
        rightSideFirstContact: 0,
        counterLeftSide: 1,
        counterRightSide: 1,
        toggleLeft: 1,
        toggleRight: 0
      };
    this.eventSource = new EventSource("http://localhost:5000/events");

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
     <div class="field">
        <Counter isLeft="1" counter={this.state.counterLeftSide} teamName={this.state.leftSideTeam} toggle={this.state.toggleLeft}/>
        <Counter isRight="1" counter={this.state.counterRightSide} teamName={this.state.rightSideTeam} toggle={this.state.toggleRight}/>
          
        <Teamview className="teamview" team={this.state.leftSideTeam} firstContact={this.state.data.leftSidefirstContact}/>
        <Teamview className="teamview" team={this.state.rightSideTeam} firstContact={this.state.data.rightSideFirstContac}/>
     </div> 
    )
}
}
export default App;
