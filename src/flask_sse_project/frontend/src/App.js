import React from 'react';
import axios from 'axios';
import Procedure from './procedure';

class App extends React.Component {
constructor(){
    super()
      this.state = {
        data: []
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
      <Procedure status='game'/>
    )
}
}
export default App;
