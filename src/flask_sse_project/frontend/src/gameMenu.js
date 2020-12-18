import React from "react";
import ButtonLine from "./buttonLine";
import ChooseField from "./chooseField"


function GameMenu (props) {

    let fowardButtonActive = false;
    let message = <h1>Choose the Game you want to play.</h1>;

    if(props.data.activeChooseField) {
        fowardButtonActive = true;
    }

    return(
        <div className="config">
            {message}
            <ChooseField activeChooseField1={props.data.activeChooseField} fieldNames={props.data.fieldNames} cursorElement={props.data.cursorElement} tableActive={true}/>
            <ButtonLine fowardButtonText="Start the Game" fowardButtonActive={fowardButtonActive}
            backwardButtonText="Back to Name-Menu" backwardButtonActive={true} cursorElement={props.data.cursorElement}/>
        </div>
    )
}

export default GameMenu