import React from "react";
import { useNavigate } from "react-router-dom";
import { createNewGame } from "../services/server";

function GameCard() {

    const navigate = useNavigate();

    async function handleCreateGame() {
        const newGameId = await createNewGame()
        navigate(`/Games/${newGameId}`)
        console.log(newGameId)
        
    }

    return(
        <>
        <h3>Game to join</h3>
        <button onClick={handleCreateGame}>Create Game</button>
        </>
    )
}

export default GameCard;