import { useEffect, useState } from "react";
import { useLoaderData } from "react-router-dom";
import { onSnapshot, doc } from "firebase/firestore";
import { db } from "../services/firbase"


export function loader( {params} ) {
    return params;
}

function Game() {

    const [hasStarted, setHasStarted] = useState(false)
    const [hasEnded, setHasEnded] = useState(false)
    const [players, setPlayers] = useState([])

    const gameId = useLoaderData().gameId;

    console.log(hasStarted)

    useEffect(() => {
        const unsub = onSnapshot(doc(db, "triviaGambleTesting", gameId), (docSnap) => {
            setHasStarted(docSnap.data().hasStarted)
            setPlayers(docSnap.data().players)
            setHasEnded(docSnap.data().hasEnded)
        })
        
        return unsub
        }, [])

        const playersArray = players.map((player, index) => {
        return <p key={index}>{player}</p>
    })

    return (
        <>
            <h1>Game: {gameId}</h1>
            {playersArray}
            
        </>
    )
}

export default Game;