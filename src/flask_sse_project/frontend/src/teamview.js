import React from "react";
const { Component } = require("react");


class Teamview extends React.Component{
    constructor() {
        super();
        this.state = {
            counter: 0,
            side: "left",
            firstContactRight: false,
            firstContactSide: "left"
        };
    }

    render() {
    const teamstyle = {
        display: "flex",
        backgroundColor: "green",
        flexGrow: "1",
        justifyContent: "center",
        borderStyle: "solid",
        borderWidth: "5px"
    };

    const counterstyle = {
        alignSelf: "center",
        fontSize: "40vh"
    };
    return (
        <div style={teamstyle}>
            <h2 style={counterstyle}>{this.props.counterTeam}</h2>
        </div>
    )
    }
}

export default Teamview