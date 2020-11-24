import React from "react";
import './teamview.css'

function Teamview (props){
    
    return (
        <div className="teamView">
            <div className="quarterField" style={{'backgroundColor': props.colorHighSite, 'opacity': props.opacityHighSite}}></div>
            <div className="quarterField" style={{'backgroundColor': props.colorDownSite, 'opacity': props.opacityDownSite}}></div>
        </div>
    )
}

export default Teamview