import React from "react";
import ButtonLine from "./buttonLine";
import "./init.css"


function ChangeSide (props) {
let message = <h1 className="message">Losing Team do you want to change Sides?</h1>

    return (
    <div className="config" >
        {message}
        <ButtonLine fowardButtonText="Change Sides" fowardButtonActive={true}
         backwardButtonText="Keep Sides" backwardButtonActive={true} cursorElement={props.data.cursorElement}/>
    </div>
    )
}
export default ChangeSide