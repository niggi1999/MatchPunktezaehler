import React from "react";
import ButtonLine from "./buttonLine";
import ChooseField from "./chooseField"


function PlayerMenu (props) {
    const fieldNames = ["1vs1", "2vs2"];

    let fowardButtonActive = false;

    if(props.activeChooseField) {
        fowardButtonActive = true;
    }

    return(
        <div className="config">
            <ChooseField activeChooseField={props.activeChooseField} fieldNames={fieldNames}/>
            <ButtonLine fowardButtonText="Press -> to continue to Player-Menu" fowardButtonActive={fowardButtonActive}
            backwardButtonText="Back to Controller Connection" backwardButtonActive={true}/>
        </div>
    )
}

export default PlayerMenu