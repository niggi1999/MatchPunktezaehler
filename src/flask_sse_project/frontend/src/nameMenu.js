import React from "react";
import ButtonLine from "./buttonLine";
import ChooseField from "./chooseField"


function NameMenu (props) {
    const fieldNames = ["Name 1", "Name 2", "Name 3", "Name 4", "Name 5", "Name 6", "Name 7", "Name 8", "Name 9", "Name 10"];

    let fowardButtonActive = false;
    let message;
    switch(props.playMode) {
        case 0:
            message = <h1>Error NameMenu!</h1>;
        case 1:
    message = <h1>Choose Your Name {props.teamName}!</h1>
            if(props.activeChooseField1) {
                fowardButtonActive = true;
            }
            break;
        case 2:
            message = <h1>Choose Your Names {props.teamName}!</h1>
            if(props.activeChooseField1 && props.activeChooseField2) {
                fowardButtonActive = true;
            }
            break;
    }

    let continueButtonMessage = "Press -> to continue to Name Selection of Team 2"
    let backButtonMessage = "Back to Player-Menu";
    if(props.teamName === "Team 2") {
        continueButtonMessage = "Press -> to continue to Game-Menu"
        backButtonMessage = "Back to Name Selection of Team 1"
    }

    return(
        <div className="config">
            {message}
            <ChooseField activeChooseField1={props.activeChooseField1} activeChooseField2={props.activeChooseField2}
            fieldNames={fieldNames} type="table"/>
            <ButtonLine fowardButtonText={continueButtonMessage}   fowardButtonActive={fowardButtonActive}
            backwardButtonText={backButtonMessage} backwardButtonActive={true}/>
        </div>
    )
}

export default NameMenu