import React from "react";
import Game from './game';
import GameMenu from "./gameMenu";
import Init from './init';
import PlayerMenu from "./playerMenu";
import NameMenu from "./nameMenu"

function Procedure (props){
    switch(props.data.status) {
        case 'init':
            return <Init data={props.data}/>;
        case 'playerMenu':
            return <PlayerMenu data={props.data}/>;
        case 'nameMenu':
            return <NameMenu data={props.data}/>;
        case 'gameMenu':
            return <GameMenu data={props.data}/>;
        case 'game':
            return <Game data={props.data}/>;
        default:
            return <h1>Invalid status. Check spelling</h1>;
    }
}

export default Procedure