import React from "react";
const { Component } = require("react");

class Counter2 extends React.Component{
    constructor() {
        super();
    }

    render() {
    
    const counterstyle2 = {
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: "10",
        width: "50%",
        height: "100%",
        position: "absolute",
        top: "0",
        right: "0",
    };

    return (
        <div style={counterstyle2}>
          <h2 style={{fontSize: "40vh"}}>{this.props.counter2}</h2>
        </div>
    )
    }
}

export default Counter2