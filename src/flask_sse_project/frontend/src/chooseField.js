import React from "react";
import "./chooseField.css"


function ChooseField (props) {

    if(props.activeChooseField1 > props.fieldNames.length) {
        return <h1>Out of Range Error</h1>;
    } 

    let cssElementList = false;
    if(props.type === "table") {
    cssElementList = props.fieldNames.map(element => 
        (props.activeChooseField1 === element
            ? 
            {
                backgroundColor: element,
                color: "white",
            }
            :
            {
                backgroundColor: "white",
                color: element,
            })
        )
    }
    else {
        cssElementList = props.fieldNames.map(element => 
            (props.activeChooseField1 === element
                ? 
                {
                    backgroundColor: "#007bff",
                    color: "white",
                }
                :
                {
                    backgroundColor: "white",
                    color: "#007bff",
                    opacity: "0.65"
                })
            )
    }
    
    let classNames = props.fieldNames.map((element) =>
        (props.type === "table" ? "chooseTableElement" : "chooseElement")
    )
    
    if(props.tableActive) {
        props.fieldNames.map((element, index) =>
        classNames[index] += (props.cursorElement === element ? " cursorElement" : "")
        )
    }

    let chooseField = props.fieldNames.map((element, index) => { 
        return(
        <div className={classNames[index]} style={cssElementList[index]}>{element}</div>) 
        })
    
    return(
        <div className={props.type === "table" ? "chooseFieldTable" : "chooseField"}>
            {chooseField.map((element) => 
                element
            )}
        </div>
    )
}

export default ChooseField