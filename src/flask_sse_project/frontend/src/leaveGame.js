import React from "react";
import ButtonLine from "./buttonLine";


function LeaveGame (props) {

    let message = "Do you want to leave the Game?"

    const style = {
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        zIndex: "20",
        width: "200px",
        height: "100px",
        position: "absolute",
        top: "0",
        left: "0"
    };

    return (
    <div>
        {message}
        <ButtonLine fowardButtonText="Leave the Game" fowardButtonActive={true}
         backwardsButtonText="Cancel" backwardsButtonActive={true} fowardButtonCursor={true} backwardButtonCursor={true}/>
    </div>
    )
}
export default LeaveGame