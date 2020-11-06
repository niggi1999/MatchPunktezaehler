import React from "react";
import './teamview.css'

class Teamview extends React.Component{
    constructor() {
        super();
        this.state = {
        };
    }

    render() {
    
    return (
        <div className="teamView">
            <div className="quarterField"></div>
            <div className="quarterField"></div>
        </div>
    )
    }
}

export default Teamview