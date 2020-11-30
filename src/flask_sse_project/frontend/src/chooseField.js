import React from "react";
import { Button } from "react-bootstrap";
import "./chooseField.css"
import 'bootstrap/dist/css/bootstrap.min.css';


function ChooseField (props) {

    let cursor = null;
    if(props.tableActive) {
        cursor = {
            borderStyle: "solid",
            borderWidth: "10px",
            borderColor: "red"
        };
    }

    if(props.activeChooseField1 > props.fieldNames.length) {
        return <h1>Out of Range Error!</h1>;
    }
    let chooseField = props.fieldNames.map((element, index) =>
        
        (props.activeChooseField1 === (index + 1) || props.activeChooseField2 === (index + 1))
            ? (<Button variant="outline-primary" style={props.cursorElement === element ? cursor : null} className={props.type === "table" ? "chooseTableElement" : "chooseElement"} active>{element}</Button>)
            : (<Button variant="outline-primary" style={props.cursorElement === element ? cursor : null} className={props.type === "table" ? "chooseTableElement" : "chooseElement"} disabled>{element}</Button>)
    )

    return(
        <div className={props.type === "table" ? "chooseFieldTable" : "chooseField"}>
            {chooseField.map((element) => 
                element
            )}
        </div>
    )
}

export default ChooseField