import React from "react";
import './teamview.css'

function Teamview (props){
    
    return (
        <div className="teamView">
            <div className="quarterField" style={{'backgroundColor': props.colorHighSite}}></div>
            <div className="quarterField" style={{'backgroundColor': props.colorDownSite}}></div>
        </div>
    )
}

export default Teamview