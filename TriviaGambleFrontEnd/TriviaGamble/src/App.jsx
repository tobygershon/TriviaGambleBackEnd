import { RouterProvider, createBrowserRouter, createRoutesFromElements, Route } from "react-router-dom"
import HomeLayout from './layouts/HomeLayout'
import BoardLayout from './layouts/BoardLayout'
import GameLayout from './layouts/GameLayout'
import NotFound from "./components/NotFound"
import Game, { loader as GameLoader} from './components/Game'
import HomePage from "./components/HomePage"


function App() {

    const router = createBrowserRouter(createRoutesFromElements(

        <Route path="/" element={<HomeLayout />} >

            <Route path="" element={<HomePage />} />

            <Route path="Board" element={<BoardLayout />} />

            <Route path="Games" element={<GameLayout />} >

                <Route path=":gameId" element={<Game />} loader={GameLoader} />

            </Route>

            <Route path="*" element={<NotFound />} />

        </Route>

    ))

    return (
        <RouterProvider router={router} />
    )
}

export default App;