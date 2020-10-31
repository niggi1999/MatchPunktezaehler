import React from "react";
import './teamview.css'
const { Component } = require("react");


class Teamview extends React.Component{
    constructor() {
        super();
        this.state = {
            side: "left",
            firstContactRight: false,
            firstContactSide: "left"
        };
    }

    render() {
    
    return (
        <div class="halfField">
            <div class="quarterField"></div>
            <div class="quarterField"></div>
        </div>
    )
    }
}

export default Teamview