import React from "react";
import "./init.css"
import ButtonLine from "./buttonLine"


function Init (props) {

    let message;
    let fowardButtonActive = false;

    switch(props.data.connectedController) {
        case 0:
            message = <h1 className="message">There is no connected Controller. Check your Bluetooth-Connection.</h1>;
            break;
        case 1:
            message = <h1 className="message">There is one connected Controller.</h1>;
            fowardButtonActive = true;
            break;
        case 2:
            message = <h1 className="message">There are two connected Controllers.</h1>;
            fowardButtonActive = true;
            break;
        default:
            message = <h1 className="message">Error</h1>;
    }

    return (
    <div className="config">
        {message}
        <ButtonLine fowardButtonText="Continue to Player-Menu" fowardButtonActive={fowardButtonActive}
         backwardsButtonText="" backwardButtonActive={false} cursorElement={props.data.cursorElement}/>
    </div>
    )
}

export default Init