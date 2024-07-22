// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore, onSnapshot, doc, updateDoc, increment, collection } from "firebase/firestore";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyA2PvV_2VQo4X6CoZ-0OacZej6xJSYPbwc",
  authDomain: "triviagamble.firebaseapp.com",
  projectId: "triviagamble",
  storageBucket: "triviagamble.appspot.com",
  messagingSenderId: "1049182867494",
  appId: "1:1049182867494:web:a331459c02d2ba4579d6e7",
  measurementId: "G-61MRHNJY22"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// Initialize Firestore
const db = getFirestore(app);

const testingCollectionRef = collection(db, "triviaGambleTesting");

export async function getScore(id) {
    const unsub = onSnapshot(doc(db, "triviaGambleTesting", id), (doc) => {
        console.log("Current data: ", doc.data());
    })

    unsub()
}

export async function addToScore(id) {
    const docRef = doc(db, "triviaGambleTesting", id);
    await updateDoc(docRef, {
        score: increment(1)
    })
    console.log('worked')
}

export async function takeAwayScore(id) {
    const docRef = doc(db, "triviaGambleTesting", id);
    await updateDoc(docRef, {
        score: increment(-1)
    })
    console.log('worked')
}