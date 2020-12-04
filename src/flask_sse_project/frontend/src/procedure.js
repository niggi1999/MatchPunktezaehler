import React from "react";
import Game from './game';
import GameMenu from "./gameMenu";
import Init from './init';
import PlayerMenu from "./playerMenu";
import NameMenu from "./nameMenu";
import LeaveGame from "./leaveGame";
import ChangeSide from './changeSide';

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
        case 'leaveGame':
            return <LeaveGame data={props.data}/>;
        case 'changeSide':
            return <ChangeSide data={props.data}/>;
        default:
            return <h1>Invalid status. Check spelling</h1>;
    }
}

export default Procedure