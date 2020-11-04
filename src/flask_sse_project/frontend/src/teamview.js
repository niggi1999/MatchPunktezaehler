import React from "react";
import './teamview.css'
const { Component } = require("react");


class Teamview extends React.Component{
    constructor() {
        super();
        this.state = {
            colorLeftSide: "white",
            colorRightSide: "white"
        };
    }

    showFirstContactField() {
        if (this.props.firstContact === 1) {
            if(this.props.firstContactField === 'left') {
                //change css
            }
            else {
                //change css
            }
        }
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