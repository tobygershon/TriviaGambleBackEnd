import { useState, useEffect } from "react";

function Timer() {

    const [seconds, setSeconds] = useState(5)
    const [isEnded, setIsEnded] = useState(false)

    function startTimer() {
        while (seconds > 0) {
            setTimeout(() => incrementTimer(), 1000)
            if (seconds === 0) {
                setIsEnded(true)
            }
        }
    }

    console.log(isEnded)

    function incrementTimer() {
        setSeconds(prev => prev - 1)
    }

    return (
        <>
        Timer
        <button onClick={startTimer} >start Timer</button>
        {seconds}
        </>
    )
}

export default Timer;