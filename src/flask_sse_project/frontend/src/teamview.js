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
    return <h2>{this.props.counterTeam}</h2>
    }
}

export default Teamview