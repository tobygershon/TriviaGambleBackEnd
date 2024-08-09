import React from 'react'
import { Outlet } from 'react-router-dom';
import Board from '../components/Board'
import About from '../components/About';
import Timer from '../components/Timer';

function HomeLayout() {

    const [startTimer, setStartTimer] = React.useState(true)
    const [reset, setReset] = React.useState(false)
    const [seconds, setSeconds] = React.useState(5)
    const [isEnded, setIsEnded] = React.useState(false)

    const intervalRef = React.useRef(0)
    React.useEffect(() => {
        const id = setInterval(() => {
            setSeconds(prev => prev - 1)
        }, 1000)
        intervalRef.current = id;
    }, [reset])

    function stopTimer(num) {
        clearInterval(num)
    }

    function toggleTimer() {
        setStartTimer(prev => !prev)
    }

    function resetTimer() {
        const intId = intervalRef.current
        clearInterval(intId)
        setSeconds(5)
        setReset(prev => !prev)
    }

    function setEnded() {
        setIsEnded(true)
    }


    return (
        <>
            <h1>Home layout</h1>
            <button onClick={toggleTimer}>open timer</button>
            {isEnded ?
                <button onClick={resetTimer} disabled>restart</button> :
                <button onClick={resetTimer}>restart</button>
            } 
            {startTimer && <Timer stopTimer={stopTimer} setIsEnded={setEnded} id={intervalRef.current} seconds={seconds}/>}
            <Outlet />
        </>
    )
}

export default HomeLayout;