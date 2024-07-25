import React from 'react'
import { Outlet } from 'react-router-dom';

function GameLayout() {

    return (
        <>
            <h1>Game Layout</h1>
            <Outlet />
        </>
    )
}

export default GameLayout;