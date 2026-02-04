// Firebase imports
import { initializeApp } from "firebase/app";
import { getAuth, signInWithPopup, GoogleAuthProvider, signOut } from "firebase/auth";

// Your Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyDdOR0UxAIv3Gtt7pUrCbHXu2Ip61qOSW0",
  authDomain: "puns--med-finder.firebaseapp.com",
  projectId: "puns--med-finder",
  storageBucket: "puns--med-finder.firebasestorage.app",
  messagingSenderId: "698903478643",
  appId: "1:698903478643:web:10bd009b3bcf45f5c9c506",
  measurementId: "G-8V9TEGKN9M"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Sign in function
export function googleSignIn() {
  signInWithPopup(auth, provider)
    .then((result) => {
      const user = result.user;
      alert(`Welcome ${user.displayName}`);
      console.log(user); // Send data to backend if needed
    })
    .catch((error) => {
      console.error("Error during sign-in:", error);
    });
}

// Sign out function
export function googleSignOut() {
  signOut(auth)
    .then(() => {
      alert("Signed out successfully.");
    })
    .catch((error) => {
      console.error("Sign-out error:", error);
    });
}