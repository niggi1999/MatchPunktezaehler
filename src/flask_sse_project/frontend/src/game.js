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
                
                <Teamview colorHighSite={props.data.team1HighColor} colorDownSite={props.data.team1DownColor}
                opacityHighSite={props.data.opacityHighSiteTeam1} opacityDownSite={props.data.opacityDownSiteTeam1}/>

                <Teamview colorHighSite={props.data.team2HighColor} colorDownSite={props.data.team2DownColor}
                opacityHighSite={props.data.opacityHighSiteTeam2} opacityDownSite={props.data.opacityDownSiteTeam2}/>

            </div>
       )
}

export default Game