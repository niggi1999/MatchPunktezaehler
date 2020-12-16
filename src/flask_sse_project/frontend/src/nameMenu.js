import React from "react";
import ButtonLine from "./buttonLine";
import ChooseField from "./chooseField";
import "./nameMenu.css"


function NameMenu (props) {

    let fowardButtonActive = false;
    let message;
    let table1Active = false;
    let table2Active = false;
    let table3Active = false;
    let table4Active = false;

    switch(props.data.playMode) {
        case 0:
            message = <h1>Error NameMenu</h1>;
            break;
        case 1:
            message = <h1>Choose Your Names</h1>
            if(props.data.color1Team1 && props.data.color1Team2) {
                fowardButtonActive = true;
            }
            switch(props.data.tableActive){
                case 1:
                    table1Active = true;
                    break;
                case 2:
                    table3Active = true;
                    break;
                default:
                    break;
            }
            break;
        case 2:
            message = <h1>Choose Your Names</h1>
            if(props.data.color1Team1 && props.data.color1Team2 && props.data.color2Team1 && props.data.color2Team2) {
                fowardButtonActive = true;
            }
            switch(props.data.tableActive) {
                case 1:
                    table1Active = true;
                    break;
                case 2:
                    table2Active = true;
                    break;
                case 3:
                    table3Active = true;
                    break;
                case 4:
                    table4Active = true;
                    break;
                default:
                    break;
            }
            break;
        default:
            message = <h1>Error NameMenu</h1>;
            break;
    }

    let continueButtonMessage = "Continue to Game Menu";
    let backButtonMessage = "Back to Player-Menu";

    return(
        <div className="config">
            {message}
            <div className="tableField">
                <div className="teamTables">
                    <h1 style={{fontSize: "75px"}}>Team 1</h1>
                        <div className="tables">
                            <ChooseField activeChooseField1={props.data.color1Team1} fieldNames={props.data.fieldNames} 
                            cursorElement={props.data.cursorElement} tableActive={table1Active} type="table"/>
                            {props.data.playMode === 2 
                            ? <ChooseField activeChooseField1={props.data.color2Team1} fieldNames={props.data.fieldNames}
                            cursorElement={props.data.cursorElement} tableActive={table2Active} type="table"/> 
                            : null}
                        </div>
                </div>
                <div className="teamTables">
                    <h1 style={{fontSize: "75px"}}>Team 2</h1>
                    <div className="tables">
                            <ChooseField activeChooseField1={props.data.color1Team2} fieldNames={props.data.fieldNames}
                            cursorElement={props.data.cursorElement} tableActive={table3Active} type="table"/>
                            {props.data.playMode === 2 
                            ? <ChooseField activeChooseField1={props.data.color2Team2} fieldNames={props.data.fieldNames}
                            cursorElement={props.data.cursorElement} tableActive={table4Active} type="table"/> 
                            : null}
                        </div>
                </div>
            </div>
            <ButtonLine fowardButtonText={continueButtonMessage} fowardButtonActive={fowardButtonActive}
            backwardButtonText={backButtonMessage} backwardButtonActive={true} cursorElement={props.data.cursorElement}/>
        </div>
    )
}

export default NameMenu