import React from "react";
import './teamview.css'

function Teamview (props){
    
    return (
        <div className="teamView">
            <div className="quarterField" style={{'backgroundColor': props.colorHighSite, 'opacity': props.opacityHighSite}}>
                <h1 style={{'fontSize': '200px', 'opacity': props.opacityHighSite === 1 ? '1' : '0'}}>+</h1>
            </div>
            <div className="quarterField" style={{'backgroundColor': props.colorDownSite, 'opacity': props.opacityDownSite}}>
                <h1 style={{'fontSize': '200px', 'opacity': props.opacityDownSite === 1 ? '1' : '0'}}>+</h1>
            </div>
        </div>
    )
}

export default Teamview