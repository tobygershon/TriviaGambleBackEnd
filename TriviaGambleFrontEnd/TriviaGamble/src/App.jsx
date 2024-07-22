import { useState, useEffect } from 'react'
import './App.css'
import { getAnswer } from './services/server'
import { addToScore, takeAwayScore } from './services/firbase'
import { initializeApp } from "firebase/app";
import { getFirestore, onSnapshot, doc } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyA2PvV_2VQo4X6CoZ-0OacZej6xJSYPbwc",
  authDomain: "triviagamble.firebaseapp.com",
  projectId: "triviagamble",
  storageBucket: "triviagamble.appspot.com",
  messagingSenderId: "1049182867494",
  appId: "1:1049182867494:web:a331459c02d2ba4579d6e7",
  measurementId: "G-61MRHNJY22"
};

function App() {
  const [score, setScore] = useState(0)
  const [answer, setAnswer] = useState('')
  const [counter, setCounter] = useState(0)

  function handleTrueClick() {
    console.log('true was clicked')
    setCounter(prev => prev + 1)
    setAnswer('true')
  }

  function handleFalseClick() {
    console.log('false was clicked')
    setCounter(prev => prev + 1)
    setAnswer('false')
  }

  function handleOther() {
    setAnswer('asdfa')
  }

  function changeScore(response) {
       if (response.data.answer === true) {
      addToScore('1') // 1 is the doc id
    } else if (response.data.answer === false) {
      takeAwayScore('1') // 1 is the doc id
    } else {
      return
    }
  }

  const app = initializeApp(firebaseConfig);
// Initialize Firestore
const db = getFirestore(app);

useEffect(() => {
const unsub = onSnapshot(doc(db, "triviaGambleTesting", '1'), (docSnap) => {
    console.log("Current data: ", docSnap.data());
    setScore(docSnap.data().score)
})

return unsub
}, [])

console.log(answer)

  useEffect(() => {
    async function get_answer() {
      const resp = await getAnswer(answer)
      changeScore(resp)
    }
    
    get_answer()
  }, [counter])



  return (
    <>
      <button onClick={handleTrueClick}>True</button>
      <button onClick={handleFalseClick}>false</button>
      <button onClick={handleOther}>other</button>

      <h1>Score</h1>
      <h3>{score}</h3>

    </>
  )
}

export default App
