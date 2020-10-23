import React, { Component } from "react";
import TeamView from "./teamview"

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: {
          counter1: 1,
          counter2: 2,
      },

      a: "hello"
    }
    this.eventSource = new EventSource("events");
  }

  componentDidMount() {
    this.eventSource.onmessage = e =>
      this.updateSite(JSON.parse(e.data));
  }

  updateSite(flightState) {
    this.setState(Object.assign({}, { data: flightState }));
  }


  render() {
    return (
      <div className="App">
        <TeamView counterTeam={this.state.data.counter1} />
        <TeamView counterTeam={this.state.data.counter2} />
        <h1>Hello World!</h1> 
      </div>
    );
  }
}

export default App;
