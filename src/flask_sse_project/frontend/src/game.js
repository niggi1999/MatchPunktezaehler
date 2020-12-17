import React from "react";
import Teamview from './teamview';
import Counter from './counter';
import './game.css';

function Game(props) {

    return (
        
            <div className="field">

                {props.data.team1Left
                ? <Counter isLeft="1" counter={props.data.counterTeam1} rounds={props.data.roundsTeam1} games={props.data.gamesTeam1}/>
                : <Counter isLeft="1" counter={props.data.counterTeam2} rounds={props.data.roundsTeam2} games={props.data.gamesTeam2}/>}

                {props.data.team1Left
                ? <Counter isRight="1" counter={props.data.counterTeam2} rounds={props.data.roundsTeam2} games={props.data.gamesTeam2}/>
                : <Counter isRight="1" counter={props.data.counterTeam1} rounds={props.data.roundsTeam1} games={props.data.gamesTeam1}/>}
                
                <Teamview colorHighSite={props.data.leftSideHighColor} colorDownSite={props.data.leftSideDownColor}
                opacityHighSite={props.data.leftSideHighColorOpacity} opacityDownSite={props.data.leftSideDownColorOpacity}/>

                <Teamview colorHighSite={props.data.rightSideHighColor} colorDownSite={props.data.rightSideDownColor}
                opacityHighSite={props.data.rightSideHighColorOpacity} opacityDownSite={props.data.rightSideDownColorOpacity}/>

            </div>
       )
}

export default Game