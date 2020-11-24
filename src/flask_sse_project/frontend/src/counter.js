import React from "react";

class Counter extends React.Component{
    constructor() {
        super();
    }

    render() {
    
    const counterstyle = {
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        zIndex: "10",
        width: "50%",
        height: "100%",
        position: "absolute",
        top: "0",
        left: this.props.isLeft ? '0' : null,
        right: this.props.isRight ? '0' : null,
    };

    return (
        <div style={counterstyle}>
            <h1 style={{'fontSize': '30px', 'fontWeight': 'bolder'}}>Won Games: {this.props.games}</h1>
            <h1 style={{'fontSize': '30px', 'fontWeight': 'bolder'}}>Won Rounds: {this.props.rounds}</h1>
            <h1 style={{'fontSize': '400px', 'fontWeight': 'bolder'}}>{this.props.counter}</h1>
        </div>
    )
    }
}

export default Counter