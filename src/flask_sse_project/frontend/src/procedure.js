import React from "react";
import Game from './game';
import GameMenu from "./gameMenu";
import Init from './init';
import PlayerMenu from "./playerMenu";

function Procedure ( {status} ){
    switch(status) {
        case 'init':
            return <Init connectedController="2" />;
        case 'playerMenu':
            return <PlayerMenu />;
        case 'gameMenu':
            return <GameMenu />;
        case 'game':
            return <Game />;
        default:
            return null;
    }


}

export default Procedure