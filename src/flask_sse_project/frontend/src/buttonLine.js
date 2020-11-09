import React from "react";
import "./buttonLine.css";
import { Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';


function ButtonLine(props) {

    let fowardButton = null;
    if(props.fowardButtonActive) {
        fowardButton = <Button variant="outline-primary" size="lg" active>{props.fowardButtonText}</Button>
    }
    else {
        fowardButton = <Button variant="outline-primary" size="lg" disabled>{props.fowardButtonText}</Button>
    }

    let backwardButton = null;
    if(props.backwardButtonActive) {
        backwardButton = <Button variant="outline-primary" size="lg" active>{props.backwardButtonText}</Button>;
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