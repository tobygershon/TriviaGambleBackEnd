import React from 'react'
import { Outlet } from 'react-router-dom';
import Board from '../components/Board'
import About from '../components/About';
import Timer from '../components/Timer';

function HomeLayout() {


    return (
        <>
        <h1>Home layout</h1>
        <Timer />
        <Outlet />
        </>
    )
}

export default HomeLayout;