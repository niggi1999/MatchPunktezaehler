import React from "react";
import Game from './game';
import GameMenu from "./gameMenu";
import Init from './init';
import PlayerMenu from "./playerMenu";
import NameMenu from "./nameMenu"

function Procedure (props){
    switch(props.data[0].status) {
        case 'init':
            return <Init connectedController={props.data[1].connectedController}/>;
        case 'playerMenu':
            return <PlayerMenu activeChooseField={props.data[2].activeChooseField}/>;
        case 'nameMenuTeam1':
            return <NameMenu playMode={props.data[3].playMode} activeChooseField1={props.data[3].activeChooseField1}
            activeChooseField2={props.data[3].activeChooseField2} teamName="Team 1"/>;
        case 'nameMenuTeam2':
            return <NameMenu playMode={props.data[4].playMode} activeChooseField1={props.data[4].activeChooseField1}
            activeChooseField2={props.data[4].activeChooseField2} teamName="Team 2"/>;
        case 'gameMenu':
            return <GameMenu activeChooseField={props.data[5].activeChooseField}/>;
        case 'game':
            return <Game counterTeam1={props.data[6].counterTeam1} counterTeam2={props.data[6].counterTeam2}/>;
        default:
            return <h1>Invalid status. Check spelling</h1>;
    }

}

export default Procedure