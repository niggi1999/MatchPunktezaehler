import React from "react";
import "./init.css"
import ButtonLine from "./buttonLine"
import ChooseField from "./chooseField"


function Init (props) {

    let message;
    let continueButton = <button className="continueButton">Press -> to go to Player Menu</button>;
    let fowardButtonActive = false;

    switch(props.connectedController) {
        case 0:
            message = <h1 className="message">There is no connected Controller. Check your Bluetooth-Connection!</h1>;
            break;
        case 1:
            message = <h1 className="message">There is one connected Controller!</h1>;
            fowardButtonActive = true;
            break;
        case 2:
            message = <h1 className="message">There are two connected Controllers!</h1>;
            fowardButtonActive = true;
            break;
        default:
            message = <h1 className="message">Error!</h1>;
    }

    return (
    <div className="config">
        {message}
        <ButtonLine fowardButtonText="Press -> to continue to Player-Menu" fowardButtonActive={fowardButtonActive}
         backwardsButtonText="" backwardsButtonActive={false}/>
    </div>
    )
}

export default Init