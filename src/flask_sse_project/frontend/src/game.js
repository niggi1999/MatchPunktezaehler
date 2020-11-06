import React from "react";
import Teamview from './teamview';
import Counter from './counter';
import './game.css';

function Game() {

    return (
        <div className="field" style={{height: "100vh"}}>
           <Counter isLeft="1" />
           <Counter isRight="0" />
             
           <Teamview />
           <Teamview />
        </div> 
       )
}

export default Game