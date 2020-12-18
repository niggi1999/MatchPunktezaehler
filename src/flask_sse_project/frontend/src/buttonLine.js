import React from "react";
import "./buttonLine.css";
import { Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';


function ButtonLine(props) {

    let cursorActiveForwardButton = {
        borderStyle: "solid",
        borderWidth: "10px",
        borderColor: "red",
        fontSize: "xx-large",
        position: "absolute",
        right: "0"
    };

    let cursorActiveBackwardButton = {
        borderStyle: "solid",
        borderWidth: "10px",
        borderColor: "red",
        fontSize: "xx-large",
        left: "0",
    };

    let backwardButtonStyle = {fontSize: "xx-large", position: "absolute", left: "0"};
    let forwardButtonStyle = {fontSize: "xx-large", position: "absolute", right: "0"};


    switch(props.cursorElement) {
        case "forwardButton":
            forwardButtonStyle = cursorActiveForwardButton;
            break;
        case "backwardButton":
            backwardButtonStyle = cursorActiveBackwardButton;
            break;
        default:
            break;
    }

    let fowardButton = null;
    if(props.fowardButtonActive) {
        fowardButton = <Button style={forwardButtonStyle} variant="outline-primary" size="lg" active>{props.fowardButtonText}</Button>
    }
    else {
        fowardButton = <Button style={forwardButtonStyle} variant="outline-primary" size="lg" disabled>{props.fowardButtonText}</Button>
    }

    let backwardButton = null;
    if(props.backwardButtonActive) {
        backwardButton = <Button style={backwardButtonStyle} variant="outline-primary" size="lg" active>{props.backwardButtonText}</Button>;
    }
    else {
        backwardButton = <div></div>;
    }
    

    return(
        <div className="buttonLine">
            {backwardButton}
            {fowardButton}
        </div>
    )
}


export default ButtonLine