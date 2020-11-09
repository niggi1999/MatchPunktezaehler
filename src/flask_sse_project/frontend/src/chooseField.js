import React from "react";
import { Button } from "react-bootstrap";
import "./chooseField.css"
import 'bootstrap/dist/css/bootstrap.min.css';


function ChooseField (props) {

    let fieldOne = <Button variant="outline-primary" className="choose" disabled>1vs1</Button>
    let fieldTwo = <Button variant="outline-primary" className="choose" disabled>2vs2</Button>

    switch(props.activeChooseField) {
        case 0:
            break;
        case 1:
            fieldOne = <Button variant="outline-primary" className="choose" active>1vs1</Button>
            break;
        case 2:
            fieldTwo = <Button variant="outline-primary" className="choose" active>2vs2</Button>
            break;
        default:
            return <h1>Error</h1>;

    }

    return(
        <div className="chooseField">
            {fieldOne}
            {fieldTwo}
        </div>
    )
}

export default ChooseField