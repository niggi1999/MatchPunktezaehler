import React from "react";
import Teamview from './teamview';
import Counter from './counter';
import './game.css';

function Game(props) {

    return (
        <div className="field">
           <Counter isLeft="1" counter={props.counterTeam1}/>
           <Counter isRight="1" counter={props.counterTeam2}/>
            
            {props.team1Left 
            ? <Teamview colorHighSite={props.team1HighColor} colorDownSite={props.team1DownColor}/>
            : <Teamview colorHighSite={props.team2HighColor} colorDownSite={props.team2DownColor}/>}

            {props.team1Left 
            ? <Teamview colorHighSite={props.team2HighColor} colorDownSite={props.team2DownColor}/>
            : <Teamview colorHighSite={props.team1HighColor} colorDownSite={props.team1DownColor}/>}

        </div> 
       )
}

export default Game