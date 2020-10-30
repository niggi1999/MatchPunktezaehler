import React from 'react';
import './App.css';
import axios from 'axios'
import Teamview from './teamview';

class App extends React.Component {
constructor(){
    super()
      this.state = {
        data: []
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
      
     <div className="app" class="flex-container">
       <Teamview className="teamview" counterTeam={this.state.data.counterTeam1} />
       <Teamview className="teamview" counterTeam={this.state.data.counterTeam2} />
     </div> 

    )
}
}
export default App;
