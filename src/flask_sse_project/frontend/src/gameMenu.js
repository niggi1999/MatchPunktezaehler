import React from "react";
import ButtonLine from "./buttonLine";
import ChooseField from "./chooseField"


function GameMenu (props) {
    const fieldNames = ["Badminton", "Tennis", "Volleyball"];

    let fowardButtonActive = false;

    if(props.activeChooseField) {
        fowardButtonActive = true;
    }

    return(
        <div className="config">
            <ChooseField activeChooseField1={props.activeChooseField} fieldNames={fieldNames}/>
            <ButtonLine fowardButtonText="Press -> to start the Game" fowardButtonActive={fowardButtonActive}
            backwardButtonText="Back to Name Selection of Team 2" backwardButtonActive={true}/>
        </div>
    )
}

export default GameMenu