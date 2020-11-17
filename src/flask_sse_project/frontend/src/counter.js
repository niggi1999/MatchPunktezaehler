import React from "react";

class Counter extends React.Component{
    constructor() {
        super();
    }

    render() {
    
    const counterstyle = {
        display: "flex",
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
            <h2 style={{'fontSize': '400px'}}>{this.props.counter}</h2>
        </div>
    )
    }
}

export default Counter