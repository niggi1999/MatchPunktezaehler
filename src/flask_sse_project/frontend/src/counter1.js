import React from "react";
const { Component } = require("react");

class Counter1 extends React.Component{
    constructor() {
        super();
    }

    render() {
    
    const counterstyle1 = {
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: "10",
        width: "50%",
        height: "100%",
        position: "absolute",
        top: "0",
        left: "0",
    };

    return (
        <div style={counterstyle1}>
          <h2 style={{fontSize: "40vh"}}>{this.props.counter1}</h2>
        </div>
    )
    }
}

export default Counter1