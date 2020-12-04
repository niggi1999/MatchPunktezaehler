import React from "react";

function Counter (props) {
    
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
        left: props.isLeft ? '0' : null,
        right: props.isRight ? '0' : null,
    };

    return (
        <div style={counterstyle}>
            <h1 style={{'fontSize': '30px', 'fontWeight': 'bolder'}}>Won Games: {props.games}</h1>
            <h1 style={{'fontSize': '30px', 'fontWeight': 'bolder'}}>Won Rounds: {props.rounds}</h1>
            <h1 style={{'fontSize': '30px', 'fontWeight': 'bolder', 'opacity': 0}}>LeerZeile</h1>
            <h1 style={{'fontSize': '400px', 'fontWeight': 'bolder'}}>{props.counter}</h1>
            <h1 style={{'fontSize': '30px', 'fontWeight': 'bolder', 'opacity': 0}}>LeerZeile</h1>
            <h1 style={{'fontSize': '30px', 'fontWeight': 'bolder', 'opacity': 0}}>Won Games: {props.games}</h1>
            <h1 style={{'fontSize': '30px', 'fontWeight': 'bolder', 'opacity': 0}}>Won Rounds: {props.rounds}</h1>
        </div>
    )
}

export default Counter