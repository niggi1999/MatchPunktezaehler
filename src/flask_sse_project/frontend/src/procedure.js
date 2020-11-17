import React from "react";
import Game from './game';
import GameMenu from "./gameMenu";
import Init from './init';
import PlayerMenu from "./playerMenu";
import NameMenu from "./nameMenu"

function Procedure (props){
    switch(props.data.status) {
        case 'init':
            return <Init connectedController={props.data.connectedController}/>;
        case 'playerMenu':
            return <PlayerMenu activeChooseField={props.data.activeChooseField}/>;
        case 'nameMenu':
            return <NameMenu playMode={props.data.playMode} activeChooseField1Team1={props.data.color1Team1}
            color2Team1={props.data.color1Team2} activeChooseField1Team2={props.data.color1Team2}
            activeChooseField2Team2={props.data.color2Team2}/>;
        case 'gameMenu':
            return <GameMenu activeChooseField={props.data.activeChooseField}/>;
        case 'game':
            return <Game counterTeam1={props.data.counterTeam1} counterTeam2={props.data.counterTeam2} team1HighColor={props.data.team1HighColor} 
            team1DownColor={props.data.team1DownColor} team2HighColor={props.data.team2HighColor} team2DownColor={props.data.team2DownColor}
            team1Left={props.data.team1Left}/>;
        default:
            return <h1>Invalid status. Check spelling</h1>;
    }

}

export default Procedure