import { useState, useEffect } from "react";

function Timer( { id, stopTimer, seconds, setIsEnded } ) {

    if (seconds === 0) {
        stopTimer(id)
        setIsEnded()
        console.log('ended')
    } 

    

    // console.log(isEnded)

    // useEffect(() => {
        
    //     setSecond(5)
        
    // }, [reset])


    // function startTimer() {
    //     console.log('start timer')
    //     let num = seconds
    //     const id = setInterval(incrementTimer, 1000)
        
    //     function incrementTimer() {
    //         if (num > 0) {
    //             setSecond(prev => prev - 1)
    //             num -= 1
    //             console.log(num)
    //             console.log(seconds)
    //             if (num === 0) {
    //                 setIsEnded(true)
    //                 clearInterval(id)
    //             }
                
    //     }
    //     }}


    return (
        <>
            Timer
            {seconds}
        </>
    )
}

export default Timer;