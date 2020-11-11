import React from "react";
import Teamview from './teamview';
import Counter from './counter';
import './game.css';

function Game(props) {

    return (
        <div className="field" style={{height: "100vh"}}>
           <Counter isLeft="1" counter={props.counterTeam1}/>
           <Counter isRight="0" counter={props.counterTeam2}/>
             
           <Teamview />
           <Teamview />
        </div> 
       )
}

export default Game