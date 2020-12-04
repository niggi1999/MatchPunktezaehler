import React from "react";
import ButtonLine from "./buttonLine";
import "./init.css"


function LeaveGame (props) {

    let message = <h1 className="message">Do you want to leave the Game?</h1>

    return (
    <div className="config" >
        {message}
        <ButtonLine fowardButtonText="Leave the Game" fowardButtonActive={true}
         backwardButtonText="Cancel" backwardButtonActive={true} cursorElement={props.data.cursorElement}/>
    </div>
    )
}
export default LeaveGame