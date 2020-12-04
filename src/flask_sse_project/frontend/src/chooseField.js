import React from "react";
import { Button } from "react-bootstrap";
import "./chooseField.css"
import 'bootstrap/dist/css/bootstrap.min.css';


function ChooseField (props) {

    if(props.activeChooseField1 > props.fieldNames.length) {
        return <h1>Out of Range Error!</h1>;
    } 

    let cssElementList = props.fieldNames.map(element => 
        (props.activeChooseField1 === element || props.activeChooseField2 === element
            ? 
            {
                backgroundColor: "#007bff",
                color: "white"
            }
            :
            {
                backgroundColor: "white",
                color: element
            })
        )

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
        <Button variant="outline-primary" className={classNames[index]} style={cssElementList[index]}>{element}</Button>) 
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