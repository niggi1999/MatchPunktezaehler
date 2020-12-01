import React from "react";
import { Button } from "react-bootstrap";
import "./chooseField.css"
import 'bootstrap/dist/css/bootstrap.min.css';


function ChooseField (props) {

    let cursor = null;
    if(props.tableActive){
        cursor = {
            borderStyle: "solid",
            borderWidth: "10px",
            borderColor: "red",
            fontSize: "xx-large",
            //color: element
        }
    }

    if(props.activeChooseField1 > props.fieldNames.length) {
        return <h1>Out of Range Error!</h1>;
    }
    
    let chooseField = props.fieldNames.map((element) =>
        
        (props.activeChooseField1 === element || props.activeChooseField2 === element)
            ? (<Button variant="outline-primary" style={props.cursorElement === element ? cursor : null}
                className={props.type === "table" ? "chooseTableElement" : "chooseElement"} active>{element}</Button>)
            : (<Button variant="outline-primary" style={props.cursorElement === element ? cursor : {"color": element}} 
                className={props.type === "table" ? "chooseTableElement" : "chooseElement"} disabled>{element}</Button>)
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