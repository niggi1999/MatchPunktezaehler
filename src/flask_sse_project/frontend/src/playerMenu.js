import React from "react";
import ButtonLine from "./buttonLine";
import ChooseField from "./chooseField"


function PlayerMenu (props) {

    let fowardButtonActive = false;

    if(props.data.activeChooseField) {
        fowardButtonActive = true;
    }

    return(
        <div className="config">
            <ChooseField activeChooseField1={props.data.activeChooseField} fieldNames={props.data.fieldNames} cursorElement={props.data.cursorElement} tableActive={true}/>
            <ButtonLine fowardButtonText="Continue to Name-Menu" fowardButtonActive={fowardButtonActive}
            backwardButtonText="Back to Controller Connection" backwardButtonActive={true} cursorElement={props.data.cursorElement}/>
        </div>
    )
}

export default PlayerMenu