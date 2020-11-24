import React from "react";
import ButtonLine from "./buttonLine";
import ChooseField from "./chooseField";
import "./nameMenu.css"


function NameMenu (props) {
    const fieldNames = ["Orange", "Red", "Purple", "Blue", "Green", "Black"];

    let fowardButtonActive = false;
    let message;
    switch(props.data.playMode) {
        case 0:
            message = <h1>Error NameMenu</h1>;
        case 1:
            message = <h1>Choose Your Names</h1>
            if(props.data.color1Team1 && props.data.color1Team2) {
                fowardButtonActive = true;
            }
            break;
        case 2:
            message = <h1>Choose Your Names</h1>
            if(props.data.color1Team1 && props.data.color1Team2 && props.data.color2Team1 && props.data.color2Team2) {
                fowardButtonActive = true;
            }
            break;
    }

    let continueButtonMessage = "Press -> to continue to Game Menu";
    let backButtonMessage = "Back to Player-Menu";

    return(
        <div className="config">
            {message}
            <div className="tableField">
                <div className="teamTables">
                    <h1>Team 1</h1>
                    <ChooseField activeChooseField1={props.data.color1Team1} activeChooseField2={props.data.color2Team1}
                    fieldNames={fieldNames} type="table"/>
                </div>

                <div className="teamTables">
                    <h1>Team 2</h1>
                    <ChooseField activeChooseField1={props.data.color1Team2} activeChooseField2={props.data.color2Team2}
                    fieldNames={fieldNames} type="table"/>
                </div>
            </div>
            <ButtonLine fowardButtonText={continueButtonMessage} fowardButtonActive={fowardButtonActive}
            backwardButtonText={backButtonMessage} backwardButtonActive={true}/>
        </div>
    )
}

export default NameMenu